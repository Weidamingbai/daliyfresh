# 文件的预处理 将txt文件形式处理成json格式
import json
import os
import pickle
import re

# 文本清洗 避免中英文字符问题
def text_clean(text):
    return text.replace(',', '，')

# 根据标点符号分割文本
def split_sents(text):
    sentences = re.split(r"([,，。 ！？?])", text)
    sentences.append("")
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    if len(sentences[-1]) == 0:  #
        sentences = sentences[:-1]
    return sentences



# 生成测试文本方法
def create_test_json(input_file,output_file):
    with open(input_file,'r',encoding="utf-8") as f:
        # 计算id
        text = f.readlines()
        json_test = []
        for i in range(len(text)):
            data_map = {}
            data_map['id'] = i
            data_map['text'] = text[i]
            json_test.append(json.dumps(data_map,ensure_ascii=False)+'\n')
    with open(output_file, 'w',encoding="utf-8") as w:
        w.writelines(json_test)



# test数据清理
def create_stride_test(input_file,output_file):
    data_list = []
    window_size = 128
    old2newid = {}
    newid2old = {}
    newidoffset = {}
    change_count = 0

    with open(input_file, 'r',encoding="utf-8") as f:
        count = 0
        for line in f:
            jdata = json.loads(line)
            text = jdata['text']
            id = jdata['id']
            # 根据标点符号切割文本
            sents = split_sents(text)
            sub_len = 0
            # 检测拆分
            for sent in sents:
                sub_len += len(sent)
            assert sub_len == len(jdata['text'])

            offset = 0
            old2newid[id] = []
            # 长度符合要求
            if len(jdata['text']) < window_size:
                sub_data = {'id': count, 'text': text}
                old2newid[id] = [count]
                newid2old[count] = id
                newidoffset[count] = offset
                count += 1
                data_list.append(json.dumps(sub_data, ensure_ascii=False) + '\n')
            else:
                change_count += 1
                s_id = 0
                s_id_max = len(sents)
                offset = 0
                while True:
                    cur_sent = ''
                    # 拼接自居
                    while s_id < s_id_max and len(sents[s_id]) + len(cur_sent) < window_size:
                        cur_sent += sents[s_id]
                        s_id += 1
                    # 生成自居
                    sub_data = {'id': count, 'text': cur_sent}
                    old2newid[id].append(count)
                    newid2old[count] = id
                    newidoffset[count] = offset
                    count += 1
                    data_list.append(json.dumps(sub_data, ensure_ascii=False) + '\n')
                    offset += len(cur_sent)

                    if s_id >= s_id_max:
                        break

    # print(f'改变原文数  {change_count} 记录数 {len(data_list)}')
    with open(output_file, 'w',encoding="utf-8") as f:
        f.writelines(data_list)


