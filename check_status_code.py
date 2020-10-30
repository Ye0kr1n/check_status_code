# -*- coding: utf-8 -*-
"""
@Time ： 2020/10/29 21:48
@Auth ： Ye0kr1n
@File ：status_codes.py
@IDE ：PyCharm
@mail:1005406456@qq.con
"""
import xlrd
import xlwt
import requests
from bs4 import BeautifulSoup
def read_xls(file):
    data = xlrd.open_workbook(file)
    table = data.sheet_by_index(0)
    dataFile = []
    ranges=0
    host=""
    print("[*]Data importing..........")
    for rowNum in range(table.nrows):
        if rowNum > 0:
            if table.row_values(rowNum)[1].find('-')==-1:       #连续端口导入
                dataFile.append(table.row_values(rowNum))
            else:
                host=table.row_values(rowNum)[0]
                ranges=table.row_values(rowNum)[1].split('-')
                for i in range(int(ranges[0]),int(ranges[1])+1,1):
                    dataFile.append([host,str(i)])
    print("[+]Data import over")
    return dataFile,len(dataFile)
def get_title(url):
    res=requests.get(url).content
    soup = BeautifulSoup(res,features="html.parser")    #使用BS4取网页标题
    title = soup.title.string
    return title

def write_xls(data):
    f = xlwt.Workbook(encoding='utf-8')     #进行文件的输出,创建sheet 创建表头,最后写入数据
    sheet1 = f.add_sheet('status_code')
    sheet1.write(0,0,"address")
    sheet1.write(0,1, "status")
    sheet1.write(0,2, "title")
    for i in range(0,len(data)):
        sheet1.write(i+1, 0, data[i][0])    #a[n][0]是ip地址,a[n][1]是响应码状态,a[n][2]是网页标题
        sheet1.write(i+1, 1, data[i][1])
        sheet1.write(i+1, 2, data[i][2])
    f.save('write_status.xls')
def check_res_code(url):
    res=""
    u=url[0]
    p=url[1]
    url="http://"+u+":"+p
    urls="https://"+u+":"+p
    title=""
    url_ans=""
    try:
        res=str(requests.get(url,timeout=0.5).status_code)    #此处做了http和https两种请求模式,取响应码
        url_ans=url
        title=get_title(url)
    except:
        try:
            res=str(requests.get(urls,timeout=0.5).status_code)
            url_ans = urls
            title=get_title(urls)
        except:
            url_ans=u+":"+p
            res="-1"
            title="Timed out"
    return [url_ans,res,title]

if __name__ == '__main__':
    readlFile = '1.xlsx'
    url_list = read_xls(readlFile)[0]
    total=read_xls(readlFile)[1]
    a=[]
    print("[+]Total:%d,timeout default:3,check status start now!!!!" %total)
    for i in range(0,len(url_list),1):
        a.append(check_res_code(url_list[i]))
    #    print(check_res_code(url_list[i]))
        print("[*][%s/%s]%s   status code:%s    title:%s"%(i+1,total,check_res_code(url_list[i])[0],check_res_code(url_list[i])[1],check_res_code(url_list[i])[2]))
    que=input("All over!!!Output to xls?[Y/n]")
    if que=='Y' or que=='':
        print("[*]Generating XLS files now......")
        write_xls(a)
        print("[+]Write OK!!!")
    else:
        exit()


