#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

import analyzedataset
import alterdata

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import os
from copy import deepcopy

def index_by_times(iterable,obj,times):
    find_times = 0
    for count,l in enumerate(iterable):
        if l == obj:
            find_times += 1
        if find_times == times:
            return count
    else :
        return -1


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_points = []
        self.selected_randoms = []
        self.random_number_type = {
                'normal': 0 ,# 高斯分布
                'uniform': 1 # 均匀分布
                # 可以添加
                }
        self.initUI()
    
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        # 需要添加一些输入模块
        line0=28
        line_start_pos = 55

        number_of_randoms_label = QLabel("请输入随机数个数",self)
        number_of_randoms_label.resize(number_of_randoms_label.sizeHint()*1.6)
        number_of_randoms_label.move(line_start_pos, line0)
        self.number_of_randoms_input = QLineEdit(None, self)
        self.number_of_randoms_input.resize(35,30)
        self.number_of_randoms_input.move(line_start_pos+111,line0)
        # ====================================
        
        random_function_label = QLabel("请选择随机数生成方式:", self)
        random_function_label.resize(random_function_label.sizeHint()*1.6)
        random_function_label.move(line_start_pos+161,line0)
        # ===================================
        
        # self.random_function_select = QRadioButton("选中为高斯分布, 否则为均匀分布", self)
        # self.random_function_select.resize(self.random_function_select.sizeHint()*1.6)
        # self.random_function_select.move(line_start_pos+300,line0-5)
        self.random_function_choose_list = QComboBox(self)
        self.random_function_choose_list.move(line_start_pos+300, line0)
        for i in self.random_number_type.keys():
            self.random_function_choose_list.addItem(i)

        # 基本常数设定
        linegap=37
        line1 = linegap+line0
        # ====================================

        # 输入文本位置的文本框提示符
        file_position_label = QLabel("请输入原始文件的位置",self)
        file_position_label.resize(file_position_label.sizeHint()*1.6)
        file_position_label.move(line_start_pos, line1)
        # ================================================

        # 用于输入文件位置的文本框 
        self.file_position_input_box = QLineEdit(None, self)
        self.file_position_input_box.move(195,line1)
        self.file_position_input_box.resize(498,30)
        # ================================================
        
        line2 = line1 + linegap
        # 选定Block的提示框
        block_name_label = QLabel("请输入Block的名称", self)
        block_name_label.resize(block_name_label.sizeHint()*1.6)
        block_name_label.move(line_start_pos, line2)

        # 输入block的文本框
        self.block_name_input = QLineEdit(None,self)
        self.block_name_input.resize(220,30)
        self.block_name_input.move(195,line2)

        # 显示数据的按钮
        show_block_data_button = QPushButton("显示数据",self)
        show_block_data_button.resize(show_block_data_button.sizeHint())
        show_block_data_button.move(195+220+60,line2)
        show_block_data_button.clicked.connect(self.show_data)

        # 更高级的方法：直接拖动 
        line3= line2 + linegap
        block_insert_label = QLabel("输入block的序数：", self)
        block_insert_label.resize(block_insert_label.sizeHint()*1.6)
        block_insert_label.move(line_start_pos,line3)
        self.block_insert = QLineEdit(None,self)
        self.block_insert.resize(55,30)
        self.block_insert.move(line_start_pos+45+71,line3)
        
       
        # 输入行位置的标签
        point_left_label = QLabel("请输入需要取的点  行：",self)
        point_left_label.resize(point_left_label.sizeHint()*1.6)
        point_left_label.move(55+115+71,line3)
        # ================================================
        
        # 字符“列”
        file_col_label = QLabel("列：",self)
        file_col_label.resize(file_position_label.sizeHint()*1.6)
        file_col_label.move(245+115+71,line3)
        # ================================================

        # 输入行位置
        self.input_box_row = QLineEdit(None,self)
        self.input_box_row.resize(45,30)
        self.input_box_row.move(195+115+71,line3)
        # ================================================

        # 输入列位置
        self.input_box_col = QLineEdit(None,self)
        self.input_box_col.resize(45,30)
        self.input_box_col.move(270+115+71,line3)
        # ================================================

        # 添加点
        add_point_button = QPushButton("+",self)
        add_point_button.setToolTip('<b>添加</b>当前输入的数据')
        add_point_button.resize(50,30)
        add_point_button.move(335+115+71,line3)
        add_point_button.setStyleSheet(r"border-radius:8px; font-size:35; border: 1px solid #84818C")
        add_point_button.clicked.connect(self.add_point)
        # ================================================

        # 删除点
        del_point_button = QPushButton("-",self)
        del_point_button.setToolTip('<b>删除</b>最后输入的数据')
        del_point_button.move(400+115+71,line3)
        del_point_button.resize(50,30)
        del_point_button.setStyleSheet(r"border-radius:8px; background-color:#FFE061; font-size:35; border: 1px solid #84818C")
        del_point_button.clicked.connect(self.del_point)
        # del_point_button.clicked.connect(...)
        # =================================================

        # 清空数据
        del_all_button = QPushButton("清空输入", self)
        del_all_button.setToolTip('<b>删除所有指定的点数据</b>')
        del_all_button.resize(del_all_button.sizeHint())
        del_all_button.setStyleSheet("background-color:red; color: white")
        del_all_button.move(125-85,422)
        del_all_button.clicked.connect(self.clearall)
        # =================================================

        # 复制部分
        line35 = line3 + linegap + 8
         # 输入随机数下限的标签
        random_left_label = QLabel("请输入需要随机数下限：",self)
        random_left_label.resize(random_left_label.sizeHint()*1.6)
        random_left_label.move(55,line35)
        # ================================================
        
        # 字符“上限”
        random_right_label = QLabel("上限:",self)
        random_right_label.resize(random_right_label.sizeHint()*1.6)
        random_right_label.move(245,line35)
        # ================================================

        # 输入下限位置
        self.input_random_left = QLineEdit(None,self)
        self.input_random_left.resize(45,30)
        self.input_random_left.move(195,line35)
        # ================================================

        # 输入上限位置
        self.input_random_right = QLineEdit(None,self)
        self.input_random_right.resize(45,30)
        self.input_random_right.move(270,line35)
        # ================================================

        # 添加点
        add_random_button = QPushButton("+",self)
        add_random_button.setToolTip('<b>添加</b>一个随机数范围')
        add_random_button.resize(50,30)
        add_random_button.move(335,line35)
        add_random_button.setStyleSheet(r"border-radius:8px; font-size:35; border: 1px solid #84818C")
        add_random_button.clicked.connect(self.add_random)
        # ================================================

        # 删除点
        del_random_button = QPushButton("-",self)
        del_random_button.setToolTip('<b>删除</b>一个随机数范围')
        del_random_button.move(400,line35)
        del_random_button.resize(50,30)
        del_random_button.setStyleSheet(r"border-radius:8px; background-color:#FFE061; font-size:35; border: 1px solid #84818C")
        del_random_button.clicked.connect(self.del_random)
        # del_point_button.clicked.connect(...)
        # =================================================


        # =================================================
        line4 = line3+ linegap + 50
        line5 = line4
        # 显示所有的点
        points_show_area_label = QLabel("已经选择的点（行，列）",self)
        points_show_area_label.resize(points_show_area_label.sizeHint()*1.6)
        points_show_area_label.move(line_start_pos-37,line4) 
        self.points_show_area = QListWidget(self)
        self.points_show_area.move(line_start_pos-45,line5+35)
        self.points_show_area.resize(150,150)

        # 显示所有的随机数
        randoms_show_area_label = QLabel("已经选择的随机数", self)
        randoms_show_area_label.resize(randoms_show_area_label.sizeHint()*1.6)
        randoms_show_area_label.move(line_start_pos+145,line4)
        self.randoms_show_area = QListWidget(self)
        self.randoms_show_area.move(line_start_pos+120,line5+35)
        self.randoms_show_area.resize(150,150)

        # 数据显示窗口
        data_show_area_label = QLabel("对应Block的数据",self)
        data_show_area_label.resize(data_show_area_label.sizeHint()*1.6)
        data_show_area_label.move(502,line4)
        self.data_show_area = QTextEdit(None,self)
        self.data_show_area.resize(365,150)
        self.data_show_area.move(line_start_pos+298,line5+35)

        # 计算用的按钮
        btn = QPushButton("生成文件", self)
        btn.setToolTip('<b>确认无误后</b>按下此按钮生成文件.')
        btn.resize(btn.sizeHint()*2)
        btn.move(534, 426)
        btn.clicked.connect(self.save_file)
        
        # 窗口部分设置
        self.setGeometry(238,118,759,517)
        self.setWindowTitle("随机数替换")
        self.show()

    def add_point(self):
        # 保证数据不能重复
        if self.input_box_row.text() and self.input_box_col.text() and self.block_name_input.text():
            point = (self.block_name_input.text(),int(self.block_insert.text() or 1),int(self.input_box_row.text()), int(self.input_box_col.text()))
            if point not in self.selected_points:
                self.selected_points.append(point)
                self.points_show_area.addItem("{}-{}: ({},{})".format(*point))
            self.input_box_row.clear()
            self.input_box_col.clear()
        # 添加能够显示数据的功能

    def del_point(self):
        if len(self.selected_points):
            current = self.points_show_area.currentRow()
            itemdeleted = self.points_show_area.takeItem(current)
            del self.selected_points[current]
            itemdeleted = None

    def add_random(self):
        if self.input_random_right.text() and self.input_random_left.text() and len(self.selected_points) > len(self.selected_randoms):
            point = (float(self.input_random_left.text()),float(self.input_random_right.text()))
            self.selected_randoms.append(point)
            self.randoms_show_area.addItem("({}, {})".format(*point))
            self.input_random_left.clear()
            self.input_random_right.clear()

    def del_random(self):
        # RESOLVED!
        if len(self.selected_randoms):
            current = self.randoms_show_area.currentRow()
            itemdeleted = self.randoms_show_area.takeItem(current)
            del self.selected_randoms[current]
            itemdeleted = None
            

    def show_data(self):
        block_str = ''
        if not self.file_position_input_box.text():
            QMessageBox.warning(self,'警告','请填入合理的文件位置',QMessageBox.Ok)
        else :
            path = self.file_position_input_box.text()
            try :
                f = analyzedataset.LoadFile(path)
            except :
                QMessageBox.warning(self,'警告','文件不存在或已经损坏，请填写正确的位置')
                return
            if f.hasContext:
                if self.block_name_input.text():
                    b = self.block_name_input.text()
                    if b in f.blocks:
                        # 可以添加block的序号
                        for count, data_block in enumerate(f[b]):
                            block_str += "block name: {} No.{}\n".format(b,count+1)
                            for row in data_block:
                                block_str += row['rawline'] + '\n'
                            block_str += '='*30 + '\n\n'
                    else :
                        block_str = "不存在的block"


                else :
                    # block 为空，输出所有的block
                    block_str = '您没有输入block，下面的Block可以供参考\n' + ' '.join(set(f.blocks))
                    block_str += '\n' + '='*30 + '\n'
                    block_str += '原始数据: \n'
                    block_str += '\n'.join(f.row_list)
            else :
                block_str = '文件已经损坏或无法打开，请检查文件名是否输入正确'
        self.data_show_area.setText(block_str)


    def clearall(self):
        if QMessageBox.warning(self, '确认', '确定要清空?', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
            self.block_name_input.clear()
            self.block_insert.clear()
            self.input_box_row.clear()
            self.input_box_col.clear()
            self.points_show_area.clear()
            self.number_of_randoms_input.clear()
            self.selected_points = []
            self.selected_randoms = []

    def save_file(self):
        if not len(self.selected_points) == len(self.selected_randoms):
            QMessageBox.warning(self,'警告','随机数的范围没有完全指定')
            return
        if not self.file_position_input_box.text():
            QMessageBox.warning(self,'警告','请填入合理的文件位置',QMessageBox.Ok)
            return
        try :
            f = analyzedataset.LoadFile(self.file_position_input_box.text())
        except :
            QMessageBox.warning(self,'警告','输入的文件无法打开',QMessageBox.Ok)
            return

        if not f.hasContext:
            QMessageBox.warning(self,'警告','文件位置输入不正确或文件已损坏',QMessageBox.Ok)
            return

        random_number_type = self.random_number_type[self.random_function_choose_list.currentText()]
        try :
            number_of_randoms = int(self.number_of_randoms_input.text())
        except :
            QMessageBox.warning(self,'警告','请输入随机数个数', QMessageBox.Ok)
            return
        # check if all number are valid
        try :
            for point in self.selected_points :
                msg = ''
                # point: block - block编号 - 行 - 列
                block_position = index_by_times(f.blocks,point[0],point[1])
                if block_position == -1:
                    msg = '发现block没有出现在文件中'
                    raise KeyError
                this_block_lines = f.data_per_block[block_position]
                this_block_rows = [i['row'] for i in this_block_lines]
                try :
                    row_position = this_block_rows.index(point[2])
                except :
                    msg = '行号超出范围'
                    raise KeyError
                if point[3] > this_block_lines[row_position]['count']:
                    msg = '列号超出范围'
                    raise KeyError

        except Exception as e :
            print(e)
            QMessageBox.warning(self,'警告','{}\n请检查block和位置的输入是否合理'.format(msg or '未知错误'),QMessageBox.Ok)
            return

        # CHECK COMPLETED,
        # GETTING AND REPLACING DATA NOW
        try :
            number_of_randoms = int(self.number_of_randoms_input.text())
        except :
            QMessageBox.warning(self,'警告','请输入合理的随机数个数',QMessageBox.Ok)
            return

        path_initial = os.path.dirname(self.file_position_input_box.text())
        folder_count = 1
        while(True):
            folder_path = os.path.join(path_initial,'{}'.format(folder_count))
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                break
            folder_count += 1


        for filecount, to_be_alterred_numbers in enumerate(alterdata.yield_dataset(self.selected_randoms,random_number_type,number_of_randoms)):
            # 注意: 随机数已经取得，正在变更数据
            data_for_change = deepcopy(f.data_per_block) # list of dicts
            for count,point in enumerate(self.selected_points) :
            # block名字 - block序号 行号 列号
                block_index = index_by_times(f.blocks,point[0],point[1])
                this_block_rows = [i['row'] for i in data_for_change[block_index]]
                row_index = this_block_rows.index(point[2])
                print(data_for_change[block_index][row_index])

                data_for_change[block_index][row_index]['data'][point[3]-1] = to_be_alterred_numbers[count]
            # data_for_change已经更改完毕
            # data_for_change和blocks等等一起可以进行文件拼写
            # 注意format格式
            # 从header开始
            str_to_be_written = '\n'.join(f.header) + '\n'
            # block_header_notion block的开头样式，直接添加即可
            for count,b in enumerate(data_for_change) :
                # b: 一个block已经更改了的数据
                str_to_be_written += f.block_header_notion[count] + '\n'
                for line_count, line_dict in enumerate(f.data_per_block[count]) :
                    str_to_be_written += line_dict['rawline'][:12] + alterdata.data_append(b[line_count]['data'],line_dict['length']) + '\n'
                str_to_be_written += '    -1\n'
            str_to_be_written += f.endjob_notion

            file_final_path = os.path.join(folder_path,'{}.inp'.format(filecount))
            with open(file_final_path,'w') as file_to_be_written:
                file_to_be_written.write(str_to_be_written)
            
            # write/save to file

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

