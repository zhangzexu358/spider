from hashlib import md5
import csv
import pymongo
import re
import os
import xlwt
import platform
import xlrd
import json

datas = list()

def get_excelinfo2(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    # 根据名字获取表
    # table = data.sheet_by_name(u'Sheet1')
    # 获取行数和列数
    nrows = table.nrows
    ncols = table.ncols

    title = ""
    fromdatas = {}
    for i in range(nrows):
        url = table.cell(i, 1).value
        if "http" in url:
            print(url)
            datas.append(url)

    #writeToExcel(datas)

def writedata(file_path):
    filelist = os.listdir(file_path)  # 列出文件夹下所有的目录与文件

    exceldatas = list()
    for i in range(0, len(filelist)):

        spider_path = os.path.join(file_path, filelist[i])

        file_name = os.path.basename(spider_path)

        content = ''
        with open(spider_path, "r", encoding='UTF-8') as f1:
            for line in f1:
                content += line

        jsonEncode = json.loads(content)
        url = jsonEncode["url"]

        if "memcount" not in jsonEncode:
            jsonEncode["memcount"] = ""
        if "tags" not in jsonEncode:
            jsonEncode["tags"] = ""
        if len(datas)>0:
            if url not in datas:
                print(url)
                exceldatas.append(jsonEncode)
            else:
                print("已存在:"+url)
    writeToExcel(exceldatas)

def writeToExcel(datas):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("group")
    #worksheet.write(0,0,u'新闻标题')
    worksheet.write(0,0,u'群名')
    worksheet.write(0,1,u'链接')
    worksheet.write(0,2,u'类型')
    worksheet.write(0,3,u'人数')
    worksheet.write(0,4,u'分类标签')
    worksheet.write(0,5, u'來源網站')
    worksheet.write(0,6, u'群备注')
    row =  1
    for data in datas:
        worksheet.write(row, 0, data['title'])
        worksheet.write(row, 1, data['url'])
        worksheet.write(row, 2, data['channel'])
        worksheet.write(row, 3, data['memcount'])
        tags = data["tags"]
        new_tag = ""
        if tags != "":
            for tag in tags:
                new_tag += str(tag)+" "
        worksheet.write(row, 4, new_tag)
        worksheet.write(row, 5, data['source'])
        worksheet.write(row, 6, data['desc'])
        row += 1

    # for data in datas:
    #     worksheet.write(row,0,data['url'])
    #     frominfo = data['frominfo']
    #
    #     #sorted(frominfo.iteritems(), key=asd: asd[0], reverse=True)
    #     if frominfo != "":
    #         d_order = sorted(frominfo.items(), key=lambda x: x[1], reverse=True)
    #         jsonstr = json.dumps(d_order,ensure_ascii=False)
    #         worksheet.write(row,1,jsonstr)
    #     else:
    #         worksheet.write(row, 1, '')
    #     row+=1

    filepath = "d:/telegram"
    if platform.system() == 'Linux':
        filepath = "/root/appnewsoutput"
    if os.path.exists(filepath)==False:
        os.makedirs(filepath)
    filename = "teledata2.xls"
    workbook.save(filepath + "/" + filename)
    # if os.path.exists(filepath):
    #     workbook.save(filepath+"/"+filename)
    # else:
    #     os.makedirs(filepath)
    #     workbook.save(filepath+"/"+filename)
    #workbook.close()
    return filepath + "/" + filename



if __name__ == '__main__':
    get_excelinfo2('Teledata.xlsx')
    writedata("E://data_ll2//Telegram")