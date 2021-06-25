# 总结NER识别流程

# 1.数据预处理 （文本长短句、生成新的文本）

# 2.加载模型

# 3.使用模型进行预测

# 4.得到预测结果 反求实体（是不是应该保存临时文件 ）
import sys
sys.path.append("..")
import json

from bert.predict import LoadModel, predict
from bert.preprocess import create_stride_test


def recognize(name, lines):
    # 传入参数 实体名 name 文本 text
    # 1.数据预处理 （文本长短句、生成新的文本）
    json_test = []
    lines = lines.split('\n')
    for i,line in enumerate(lines):
        data_map = {}
        data_map['id'] = i
        data_map['text'] = line
        json_test.append(json.dumps(data_map,ensure_ascii=False)+'\n')
    with open('/content/drive/MyDrive/ner/datasets/test.json', 'w',encoding="utf-8") as w:
        w.writelines(json_test)
    # 数据清洗
    create_stride_test('/content/drive/MyDrive/ner/datasets/test.json','/content/drive/MyDrive/ner/datasets/test.json')
    # 加载模型
    model,tokenizers = LoadModel()
    test_submit = predict(model,tokenizers)
    print(test_submit[9]['label'].get('name'))
    result_addr = []
    result_name = []
    result_company = []
    print(len(test_submit))
    for i in range(len(test_submit)):      
      if test_submit[i]['label'].get('address'):
        result_addr.append(test_submit[i]['label'].get('address'))
      elif test_submit[i]['label'].get('name'):
        result_name.append(test_submit[i]['label'].get('name'))
      elif test_submit[i]['label'].get('company'):
        result_company.append(test_submit[i]['label'].get('company'))
      else:
        continue
    return result_addr,result_name,result_company
    # if name == 'address':
    #   return result_addr
    # elif name == "name":
    #   return result_name
    # elif name == "company":
    #   result_company


# if __name__ == "__main__":
#   with open("/content/drive/MyDrive/ner/datasets/test.txt",'r',encoding="utf-8") as f:
#     lines = f.read()
#   result_addr,result_name,result_company = recognize('name',lines)
#   print(result_addr[:100])
#   print(result_name[:100])
#   print(result_company[:100])
  