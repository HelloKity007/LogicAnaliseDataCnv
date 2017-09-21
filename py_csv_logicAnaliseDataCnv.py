#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf-8
# author=&pgz

import csv

# 配置
Infile1 = 'PC-VMC'  # csv file(省略后缀名)
Infile2 = 'VMC-PC'  # csv file(省略后缀名)
CombineFile = 'PCvVMC_Combine'
bAddDataIdx = True  # csv中的数据项是否增加下标


# 将逻辑分析仪原始的csv文件数据，按帧数据合并后输出文件(离上面要两个顶角空行)
def CnvRawData2Frame(Infile, OutFile):
    with open(Infile + '.csv', 'rt') as rf:
        reader = csv.reader(rf)
        with open(OutFile + '.csv', 'at') as wf:
            writer = csv.writer(wf)
            oneFrame = []
            time_start = 0
            time_start_str = ''
            data_str = ''
            dataIdx = 0
            for i, row in enumerate(reader):
                if i > 0:
                    time = float(row[0].replace('s', ''))
                    time_str = row[0].replace('s', '')
                    data = row[1]
                if i == 0:
                    title = ['T-Start[s]', 'T-End[s]', 'frame']
                    writer.writerow(title)  # 写入第1行标题
                elif i == 1:
                    dataIdx = 0
                    time_start = time
                    time_start_str = time_str
                    oneFrame.append(time_str)
                    data_str += data + '(' + 'Y' + str(dataIdx) + ')'
                elif time - time_start < 0.0020:
                    dataIdx += 1  # 下标递增1
                    data_str += ' ' + data + '(' + 'Y' + str(dataIdx) + ')'
                    time_start = time
                    time_start_str = time_str
                else:
                    oneFrame.append(time_start_str)  # 上一次start time为上一帧结束时间
                    oneFrame.append(data_str)
                    writer.writerow(oneFrame)  # 写入文件
                    oneFrame = []  # 清空，准备开始新的一帧
                    data_str = ''  # 清空，准备开始新的一帧

                    # 记录新的一帧开始
                    dataIdx = 0  # 下一帧，从新开始计算下标
                    time_start = time
                    time_start_str = time_str
                    oneFrame.append(time_str)
                    data_str += data + '(' + 'Y' + str(dataIdx) + ')'

            oneFrame.append(data_str)
            writer.writerow(oneFrame)  # 写入文件

    print('CnvRawData2Frame ok: ' + Infile + ' ' + OutFile)


# 合并两个csv文件中的项目，按时间排序(离上面要两个顶角空行)
def CombineCsvByTime(file1, file2, OutFile):
    print("file1:" + file1)
    print("file2:" + file2)
    with open(file1 + '.csv', 'rt') as rf1:
        reader1 = csv.reader(rf1)
        rowsFile1 = [row1 for row1 in reader1]
        with open(file2 + '.csv', 'rt') as rf2:
            reader2 = csv.reader(rf2)
            rowsFile2 = [row2 for row2 in reader2]
            with open(OutFile + '.csv', 'at') as wf:
                writer = csv.writer(wf)
                idx_stTime = 0
                idx_endTime = 1
                idx_direct = 2
                idx_frame = 3
                title = ['T-Start[s]', 'T-End[s]', 'Direct', 'frame']
                writer.writerow(title)  # 写入第1行标题

                del rowsFile1[0]  # 删除标题行
                del rowsFile2[0]  # 删除标题行

                rowsFile1.reverse()  # 倒序，为利用pop
                rowsFile2.reverse()  # 倒序，为利用pop

                row_file1 = []
                row_file2 = []
                while len(rowsFile1) > 0 or len(rowsFile2) > 0:
                    # 取出file1的一行
                    if len(rowsFile1) > 0 and row_file1 == []:
                        row_file1 = rowsFile1.pop()
                        # print(row_file1)

                    # 取出file2的一行
                    if len(rowsFile2) > 0 and len(row_file2) == 0:
                        row_file2 = rowsFile2.pop()
                        # print(row_file2)

                    if len(row_file1) == 0 and len(row_file2) == 0:
                        continue
                    elif len(row_file1) == 0 and len(row_file2) != 0:
                        row_file2.insert(
                            idx_direct, file2.replace('_temp', ''))
                        writer.writerow(row_file2)
                        row_file2 = []  # 清空buf，以便取出下一行
                    elif len(row_file1) != 0 and len(row_file2) == 0:
                        row_file1.insert(
                            idx_direct, file1.replace('_temp', ''))
                        writer.writerow(row_file1)
                        row_file1 = []  # 清空buf，以便取出下一行
                    elif 1:
                        stTime1 = float(row_file1[idx_stTime])
                        stTime2 = float(row_file2[idx_stTime])
                        if stTime1 < stTime2:
                            row_file1.insert(
                                idx_direct, file1.replace('_temp', ''))
                            writer.writerow(row_file1)
                            row_file1 = []  # 清空buf，以便取出下一行
                        else:
                            row_file2.insert(
                                idx_direct, file2.replace('_temp', ''))
                            writer.writerow(row_file2)
                            row_file2 = []  # 清空buf，以便取出下一行


# 主函数(离上面要两个顶角空行)
def main():
    print("main")
    temp1 = Infile1 + '_temp'
    temp2 = Infile2 + '_temp'
    CnvRawData2Frame(Infile1, temp1)
    CnvRawData2Frame(Infile2, temp2)
    CombineCsvByTime(temp1, temp2, CombineFile)


# 程序执行入口(离上面要两个顶角空行)
if __name__ == '__main__':
    main()
