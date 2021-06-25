import sys
sys.path.append('..')
import argparse
import json
import os

import torch
from torch.utils.data import SequentialSampler, DataLoader, TensorDataset
from torch.utils.data.distributed import DistributedSampler

from processors.ner_seq import ner_processors as processors, collate_fn, convert_examples_to_features
from models.bert_tokenizer import CNerTokenizer
from models.transformers import BertConfig
from models.bert_for_ner import BertLSTMCRF
from processors.utils_ner import get_entities
from utils.common import json_to_text
from utils.progressbar import ProgressBar

                   
#任务名称
task_name = 'cluener'
# GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 数据源
data_dir = "../datasets/mixed/comp"
# 最大长度
eval_max_seq_length =512
# 实例化对象 加载标签
processor = processors[task_name]()
label_list = processor.get_labels()
id2label = {i: label for i, label in enumerate(label_list)}
label2id = {label: i for i, label in enumerate(label_list)}
num_labels = len(label_list)


def load_and_cache_examples(tokenizer,data_type):

    processor = processors[task_name]()
    examples = processor.get_test_examples(data_dir)
    label_list = processor.get_labels()
    features = convert_examples_to_features(examples=examples,
                                            tokenizer=tokenizer,
                                            label_list=label_list,
                                            max_seq_length=eval_max_seq_length,
                                            cls_token_at_end=False,
                                            pad_on_left=False,
                                            cls_token=tokenizer.cls_token,
                                            cls_token_segment_id=0,
                                            sep_token=tokenizer.sep_token,
                                            # pad on the left for xlnet
                                            pad_token=tokenizer.convert_tokens_to_ids([tokenizer.pad_token])[0],
                                            pad_token_segment_id=0,
                                            )



    # Convert to Tensors and build dataset
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    all_label_ids = torch.tensor([f.label_ids for f in features], dtype=torch.long)
    all_lens = torch.tensor([f.input_len for f in features], dtype=torch.long)
    # 对tensor类型数据进行打包 得到能够被dataload的dataset
    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_lens, all_label_ids)
    return dataset


def predict(model, tokenizer):

    # 加载数据集
    test_dataset = load_and_cache_examples(tokenizer, data_type='test')
    test_sampler = SequentialSampler(test_dataset)
    test_dataloader = DataLoader(test_dataset, sampler=test_sampler, batch_size=1, collate_fn=collate_fn)
    results = []

    for step,batch in enumerate(test_dataloader):
        model.eval()
        batch = tuple(t.to(device) for t in batch)
        with torch.no_grad():
            inputs = {"input_ids": batch[0], "attention_mask": batch[1], "labels": None, 'input_lens': batch[4]}
            # XLM and RoBERTa don"t use segment_ids
            inputs["token_type_ids"] = batch[2]
        outputs = model(**inputs)
        logits = outputs[0]
        tags = model.crf.decode(logits, inputs['attention_mask'])
        tags = tags.squeeze(0).cpu().numpy().tolist()
        preds = tags[0][1:-1]  # [CLS]XXXX[SEP]
        label_entities = get_entities(preds, id2label)
        json_d = {}
        json_d['id'] = step
        json_d['tag_seq'] = " ".join([id2label[x] for x in preds])
        # 获得了实体和位置
        json_d['entities'] = label_entities
        results.append(json_d)

    # 将预测值变回实体
    # 输入文件读取
    test_text = []
    with open(os.path.join(data_dir, "test.json"), 'r') as fr:
        for line in fr:
            test_text.append(json.loads(line))

    test_submit = []
    for x, y in zip(test_text, results):
        json_d = {}
        json_d['id'] = x['id']
        json_d['label'] = {}
        entities = y['entities']
        words = list(x['text'])
        if len(entities) != 0:
            for subject in entities:
                tag = subject[0]
                start = subject[1]
                end = subject[2]
                word = "".join(words[start:end + 1])
                if tag in json_d['label']:
                    if word in json_d['label'][tag]:
                        json_d['label'][tag][word].append([start, end])
                    else:
                        json_d['label'][tag][word] = [[start, end]]
                else:
                    json_d['label'][tag] = {}
                    json_d['label'][tag][word] = [[start, end]]
        test_submit.append(json_d)
    return test_submit


def singleton(cls):
    # 单下划线的作用是这个变量只能在当前模块里访问,仅仅是一种提示作用
    # 创建一个字典用来保存类的实例对象
    _instance = {}

    def _singleton(*args, **kwargs):
        # 先判断这个类有没有对象
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)  # 创建一个对象,并保存到字典当中
        # 将实例对象返回
        return _instance[cls]

    return _singleton

@singleton
class LoadModel:
    def __new__(cls, *args, **kwargs):
        # 加载模型（此种加载方式 依赖了pytorch环境）
        config = BertConfig.from_pretrained("./best_eval_checkpoint", num_labels=num_labels)
        tokenizer = CNerTokenizer.from_pretrained("./best_eval_checkpoint", do_lower_case=True)
        # model = BertLSTMCRF.from_pretrained(args.model_name_or_path, from_tf=bool(".ckpt" in args.model_name_or_path),
                                            #  config=config, cache_dir=args.cache_dir if args.cache_dir else None)

        model_dict = torch.load("./best_eval_checkpoint/train_model.pth")
        # 进行测试
        model = BertLSTMCRF(config)
        model.load_state_dict(model_dict)
        model.to(device)
        return model,tokenizer
