#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from copy import deepcopy
import sys

class LoadFile(object):
    '''
    用于读取文件的类
    blocks: 所有的模块
    '''
    def __init__(self,path,sep=' '):
        self.path_initial_file = path
        self.blocks = []
        self.data_per_block = []
        self.block_header_notion = []
        # data_per_block是一个列表 data_per_block -> 每个list表示一个block的所有数字 -> list中的字典表示一行数据
        # 不通过字典的形式 改成list
        # 声明私有&只读变量
        self.__sep = sep


        # 完整的读入文档
        # try :
        f = open(path,'r')
        self.row_list = [line.rstrip() for line in f.readlines()]
        self.hasContext = True
        self.splitBlocks()
        '''
        except Exception as e :
            print(e)
            self.row_list = "文件无法打开，请检查路径是否正确"
            self.hasContext = False
        '''

    @property
    def sep(self):
        return self.__sep


    def splitBlocks(self):
        # 结构：data_per_block 的每个列表是一个block的所有元素
        self.header = self.row_list[:3]
        data_without_header = deepcopy(self.row_list[3:])
        for line_total in data_without_header :
            # No in-place changes are allowed.
            line_total.rstrip()
            if self.__sep == ' ' :
                line = line_total.split()
            else :
                line = line_total.split(self.__sep)
            if not line[0].isdigit(): # 包括了-1和字母
                if not '-1' in line[0]:
                    # block的开头
                    if 'ENDJOB' in line[0] :
                        self.endjob_notion = line_total
                        continue
                    self.blocks.append(line[0])
                    self.block_header_notion.append(line_total)
                    this_block = [] # 清空block
                    # line:元素个数 line_total:总长度

                else :
                    # 发现了-1，一个block已经解析完毕
                    self.data_per_block.append(this_block)
                    
            else :
                # 数字
                # 解析黏连的数据 从1开始（第二个数字就要开始

                # 防止第一个数就出现问题
                number_of_numbers = int(line_total[6:12])
                if len(line[1])>6 :
                    item2 = line[1][number_of_numbers :]
                    item1 = str(number_of_numbers)
                    line[1] = item1
                    line.insert(2,item2)

                '''
                try :
                    number_of_numbers = int(line[1])
                except :
                    # insert 向左！ fuck
                    data = line[1]
                    line[1] = data[:1]
                    line.insert(2,data[1:])
                    line_total = ' '.join(line)

                number_of_numbers = int(line[1])

                # 方案二，能够防止第一个数出问题而且数据数量大于10，待完善，目前不用
                if number_of_numbers > 99 :
                    data = line[1]
                    line[1] = data[:1]
                    line.insert(2,data[1:])
                    line_total = ' '.join(line)
                '''
# 注意数据第一个就黏连会导致line_total 的长度和预期不同
                position1 = line_total.index(line[0]) + len(line[0])
                # position1指向第二个元素开始的第一个
                position2 = line_total[position1:].index(line[1]) + len(line[1])
                length_of_data = len(line_total) - position2 - position1
                this_block_length = int(length_of_data / number_of_numbers)
                for i in range(2,number_of_numbers+2):
                    if len(line[i]) > this_block_length:
                        # 需要拆开
                        item1 = line[i][: -this_block_length]
                        item2 = line[i][-this_block_length:]
                        line[i] = item1
                        line.insert(i+1,item2)


                block_datas = {'row':int(line[0]),'count':int(number_of_numbers),'data':[float(line[i+2].replace('D','E'))  for i in range(int(number_of_numbers))] if int(number_of_numbers)!=0 else [],'rawline':line_total,'length':this_block_length} # block_datas 一行的数字
                this_block.append(block_datas)
                

# 这里结构有点混乱 需要重新修改结构 确保data

    def getData(self):
        return deepcopy(self.row_list)

    def __getitem__(self, key):
        datas = []
        for count, block_name in enumerate(self.blocks):
            if block_name == key :
                datas.append(self.data_per_block[count])
        return datas

    

def main():
    path = "/Users/wangtianmin/Downloads/test.inp"
    ins = LoadFile(path)
    print(ins.hasContext)
    if ins.hasContext:
        print(ins['COOLIN'])
if __name__ == "__main__":
    main()


