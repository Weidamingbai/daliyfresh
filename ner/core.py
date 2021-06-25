# cmd.py
# 1. 定义接口描述
"""Num accumulator.

Usage:
  core.py <file> <entity>

  core.py (-h | --help)

Options:
  -h --help     Show help.
  --sum         Sum the nums (default: find the max).
  --input_file  inpput must be a full file path
  --entity      entity is our to find
"""
import json
import re

from docopt import docopt
from libs.date import Date
from libs.enterprise import Enterprise
from libs.internet import Internet
from libs.keys_or_token import Keys_or_token
from libs.misc import Misc
from libs.pii import Pii



dict ={
    'date': Date.finddate,
    'credit': Enterprise.findcredit,
    'tax' : Enterprise.findtax,
    'Business': Enterprise.findbusiness,
    'organization': Enterprise.findorganization,
    'ip': Internet.findip,
    'ipv6': Internet.findipv6,
    'mac': Internet.findmac,
    'url': Internet.findurl,
    'md5': Keys_or_token.findmd5,
    'jdbc': Misc.findjdbc,
    'bankcard': Pii.findbankcard,
    'id': Pii.findid,
    'carnum': Pii.findcarnum,
    'email': Pii.findemail,
    'phone': Pii.findphone,
    'telephone': Pii.findtelephone,
    'vin': Pii.findvin
}

def read_file(file):
    # 1.切分文件路径
    file_type = file.split('.')[-1]
    if file_type == "txt":
        with open(file,'r',encoding='utf-8') as f:
            lines = f.read()
    elif file_type == "json":
        with open(file,'r',encoding='utf-8') as f:
            lines = json.load(f)
    else:
        print("cannot support！")
    return lines

# 生成分词传给recognize
def split(lines):

    list = lines.split('\n')
    # 过滤不可见字符
    for i in range(len(list)):
         list[i] = re.sub('\W+', ' ', list[i]).strip()
    return list
def split_text(lines):
    pattern = ',|\\n|;|\"|\t|<|>'
    req_list = []
    resp_list = []
    for i,val in enumerate(lines['RECORDS']):
        req_content_ascii = val['req_content_ascii']
        resp_content_ascii = val['resp_content_ascii']
        req_content_ascii = re.split(pattern,req_content_ascii)
        resp_content_ascii = re.split(pattern,resp_content_ascii)
        for j, val2 in enumerate(req_content_ascii):
            req_list.append(val2)
        for j, val2 in enumerate(resp_content_ascii):
            resp_list.append(val2)
    return req_list, resp_list

def main():
    # 1.读取文件

    file = arguments['<file>']
    lines = read_file(file)

    # 2.文本预处理 简单分词
    # list = split(lines)
    req_list,resp_list = split_text(lines=lines)

    # 3.查找实体
    entity = arguments['<entity>']
    recognizer = dict[entity]

    # results = []
    req_result = []
    resp_result = []

    # for i,val in  enumerate(list):
    #     result = recognizer(text=val)
    #     if  result:
    #         results.append(result)

    for i,val in enumerate(req_list):
        result = recognizer(text=val)
        if  result:
            req_result.append(result)
    for i,val in enumerate(resp_list):
        result = recognizer(text=val)
        if  result:
            resp_result.append(result)

    # #4.组织结果返回
    # print(results)


    print(req_result)
    print(resp_result)


if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True)
    main()
"""
python  core.py 路径+文件名 实体名 
"""




