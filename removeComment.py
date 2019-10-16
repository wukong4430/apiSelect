#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name    : removeComment.py
# Author       : Kicc <kiccshen@whu.edu.cn>
# Create Date  : 2019-10-08 18:57:21
# Last Modified: 2019-10-08 18:57:21
#! coding=utf-8
import os
import re
import json
import io
"""

"""

def deal_line_python(line, flag):
    # 先判断是不是还在上一个块注释里
    if not flag:
        if '"""' in line:
            return '', True
        else:
            return '', False

    # 找到"""  """
    if '"""' in line:
        idx = line.index('"""')
        try:
            idx2 = line.index('"""', idx+1) # 单行的块注释
            new_line = ''
            return new_line, True
        except Exception as e:
            flag = False # 表示块注释没有终止
            return '', flag
    

    # 找到#
    if '#' in line:
        idx = line.index('#')
        new_line = line[:idx]
        return new_line, True

    # 没有注释的话
    return line, True


def deal_line_java(line, flag):

    # 先判断是不是还在上一个块注释里
    if not flag:
        if '*/' in line:
            return '', True
        else:
            return '', False

    # 找到/* */
    if '/*' in line:
        idx = line.index('/*')
        try:
            idx2 = line.index('*/', idx+1) # 单行的块注释
            new_line = ''
            return new_line, True
        except Exception as e:
            return '', False

    # 找到//
    if '//' in line:
       idx = line.index('//')
       new_line = line[:idx]
       return new_line, True

    # 没有注释的话
    return line, True

def deal_whole_code(code, lang):
    splits = code.split('\n')
    flag = True
    result = []
    if lang=='java':
        for line in splits:
            new_line, flag = deal_line_java(line, flag)
            result.append(new_line)
    elif lang=='python':
        for line in splits:
            new_line, flag = deal_line_python(line, flag)
            result.append(new_line)

    res = '\n'.join(result)
    return res

# 标识状态
S_INIT = 0
S_SLASH = 1

def main():
    flag = True
    path = '2016.file'
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    # print(data[0]['java'])
    origin_java = data[3]['java']
    splits = origin_java.split('\n')
    # print(splits)
    # print(data[2]['java'])

    # 输入是一个java/python 代码（带注释的） 这里的splits
    # 输出是一个java/python 代码（不带注释的）result


    res = deal_whole_code(origin_java, 'java')
    print(res)


if __name__ == '__main__':
    print('*'*40)
    main()

