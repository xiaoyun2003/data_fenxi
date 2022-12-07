import pandas as pd
import matplotlib.pyplot as plt 



#读取xlsx所有数据
def read_xlsx(file,sheet):
    df = pd.read_excel(file,sheet_name=sheet)
    return df
#读取csv文件
def read_csv(file):
    cv=pd.read_csv(file)
    return cv
#生成柱状统计图,支持多维
class Bar:
    def __init__(self,title,xname,yname):
        plt.xlabel(xname)
        plt.ylabel(yname)
        plt.title(title)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    def make(self,x,y,label="",facecolor="red",width=1):
        plt.bar(x, y, facecolor=facecolor, width=width, label = label)
    def show(self):
        plt.legend()
        plt.show()


#生成折线统计图,支持多维
class Plot:
    def __init__(self,title,xname,yname):
        plt.xlabel(xname)
        plt.ylabel(yname)
        plt.title(title)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    def make(self,x,y,color="red",label=""):
        plt.plot(x, y,c=color, marker='o', mec='r', mfc='w',label=label)
    def show(self):
        plt.legend()
        plt.show()

#生成扇形统计图
class Pie:
    def __init__(self,title):
        plt.title(title)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    def make(self,percents,labels,colors,explodes):
        plt.pie(percents,labels=labels,explode=explodes,colors=colors,autopct="%.2f%%",)
        plt.axis('equal')
    def show(self):
        plt.legend()
        plt.show()


#生成散点统计图,支持多维
class Scatter:
    def __init__(self,title,xname,yname):
        plt.xlabel(xname)
        plt.ylabel(yname)
        plt.title(title)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    def make(self,x,y,color="red",label=""):
        plt.scatter(x, y, c=color,label=label) 
    def show(self):
        plt.legend()
        plt.show()

#通用规则加法计算器,按照给定列名合并计算，并降序排序
def SUM_DATA(data,column,sum_column,sub_column=None,listnum=-1,paixu_key="trotal"):
    tmp={}
    all=0
   
    for i in data.values:
        if sub_column!=None:
            if i[column] in tmp:
                if i[sub_column] in tmp[i[column]]:
                    tmp[i[column]][i[sub_column]]=tmp[i[column]][i[sub_column]]+round(i[sum_column],3)
                else:
                    tmp[i[column]][i[sub_column]]=i[sum_column]
                if "total" in tmp[i[column]]:
                    tmp[i[column]]["total"]=tmp[i[column]]["total"]+round(i[sum_column],3)
                else:
                    tmp[i[column]]["total"]=i[sum_column] 
            else:
                sub_tmp={}
                sub_tmp[i[sub_column]]=i[sum_column]
                tmp[i[column]]=sub_tmp
                tmp[i[column]]["total"]=i[sum_column]
            all=all+i[sum_column]
        else:
            if i[column] in tmp:
                tmp[i[column]]=round(i[sum_column],3)+ tmp[i[column]]
                all=round(i[sum_column],3)+all
            else:
                tmp[i[column]]=round(i[sum_column],3)
                all=round(i[sum_column],3)+all
    if sub_column!=None:
        tmp_list= sorted(tmp.items(), key=lambda item: item[1][paixu_key], reverse=True)
    else:
        tmp_list= sorted(tmp.items(), key=lambda item: item[paixu_key], reverse=True)
    if listnum!=-1:
        tmp_list=tmp_list[:listnum]
    return (tmp_list,all)
#通用计数器,对count_column进行计数统计,如果merge_count为None只对count_column进行统计，否则根据merge_column进行合并后在统计并降序排序
def COUNT_DATA(data,count_column,sub_column=None,merge_column=None,listnum=-1,paixu_key="total"):
    tmp={}
    all=0
    if merge_column!=None:
        datatmp={}
        for i in data.values:
            datatmp[i[merge_column]]=i[count_column]
        if sub_column!=None:
            print("merge和sub方法不可以同用")
            return (None,None)
        for k,v in datatmp.items():
            if v in tmp:
                all=all+1
                tmp[v]=tmp[v]+1
            else:
                all=all+1
                tmp[v]=1
    else:
        for i in data.values:
            if sub_column!=None:
                if i[count_column] in tmp:
                    tmp[i[count_column]]["total"]=tmp[i[count_column]]["total"]+1
                    if i[sub_column] in tmp[i[count_column]]:
                        tmp[i[count_column]][i[sub_column]]=tmp[i[count_column]][i[sub_column]]+1 
                    else:
                        tmp[i[count_column]][i[sub_column]]=1
                else:
                    sub_tmp={}
                    sub_tmp[i[sub_column]]=1
                    sub_tmp["total"]=1
                    tmp[i[count_column]]=sub_tmp
                all+=1
            else:

                if i[count_column] in tmp:
                    all=all+1
                    tmp[i[count_column]]=tmp[i[count_column]]+1
                else:
                    all=all+1
                    tmp[i[count_column]]=1
    
    if sub_column!=None:
        tmp_list= sorted(tmp.items(), key=lambda item: item[1][paixu_key], reverse=True)
    else:
        tmp_list= sorted(tmp.items(), key=lambda item: item[paixu_key], reverse=True)
    if listnum==-1:
        return (tmp_list,all)
    else:
        return (tmp_list[:listnum],all)
#


#设置数据文件
XLSX_FILE="2019.xlsx"
XLSX_SHEET="Sheet1"
CSV_FILE="2020ABC.csv"
xlsx_data=read_xlsx(XLSX_FILE,XLSX_SHEET)
csv_data=read_csv(CSV_FILE)


def t1():
    obj_total_price,objAllPrice=SUM_DATA(xlsx_data,0,3,paixu_key=1)
    labels=[]
    percents=[]
    for i in obj_total_price:
        k=i[0]
        v=i[1]
        labels.append(k)
        percents.append(v/objAllPrice*100)
    color =[ "red" if i%3==0 else "green" if i%3==1 else "blue" if i%3==2 else "red" for i in range(len(labels))]
    explode=[0 for i in range(len(percents))]
    #画图
    pie=Pie("商品交易总额月份占比扇形图")
    pie.make(percents,labels,colors=color,explodes=explode)
    pie.show()

def t2():
    obj_total_price,_=SUM_DATA(xlsx_data,1,3,listnum=9,paixu_key=1)
    x=[]
    y=[]
    for i in obj_total_price:
        k=i[0]
        v=i[1]
        x.append(k)
        y.append(v)
    #画图
    pie=Bar("商品交易总额前九排名柱状图","商品名称","总交易额")
    pie.make(x,y,width=0.5)
    pie.show()




def t3():
    res,total=COUNT_DATA(csv_data,18,merge_column=4,paixu_key=1)
    percents=[]
    labels=[]
    for i in res:
        k=i[0]
        v=i[1]
        print(v)
        percents.append(v/total*100)
        labels.append(k)
    pie=Pie("顾客类型占比扇形图")
    pie.make(percents,labels,colors=["red","blue","green"],explodes=[0,0,0.1])
    pie.show()




def t4():
    x=[]
    y=[]
    x1=[]
    y1=[]
    for k,v in SUM_DATA(xlsx_data,0,3,paixu_key=0)[0]:
        x1.append(k)
        y1.append(v)
    for k,v in SUM_DATA(xlsx_data,0,2,paixu_key=0)[0]:
        x.append(k)
        y.append(v)
    plot=Plot("月份交易数量与总额折线图","月份","数量")
    plot.make(x,y,label="交易数量")
    plot.make(x1,y1,"blue",label="交易额")
    plot.show()

def t5():
    x=[]
    y=[]
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    for k,v in COUNT_DATA(csv_data,11,18)[0]:
        x.append(k)
        x1.append(k)
        x2.append(k)
        y.append(v["头部顾客"])
        y1.append(v["腰部顾客"])
        y2.append(v["尾部顾客"])
    plot=Scatter("不同月份顾客类型散点","月份","顾客类型")
    plot.make(x,y,label="头部顾客")
    plot.make(x1,y1,"blue",label="腰部顾客")
    plot.make(x2,y2,"green",label="尾部顾客")
    plot.show()
def t6():
    res,al=COUNT_DATA(csv_data,16,merge_column=4,paixu_key=0)
    x=[]
    y=[]
    for i in res:
        x.append(i[0])
        y.append(i[1])

    plot=Plot("不同时段用户数量折线图","时间","用户数量")
    plot.make(x,y,label="时段用户数")
    plot.show()

def t7():
    res,_=COUNT_DATA(csv_data,4,paixu_key=1)
    res1,_=SUM_DATA(csv_data,4,sum_column=7,listnum=9,paixu_key=1)
    x=[]
    y=[]
    x1=[]
    y1=[]
    r={}
    for i in res1:
        t=[0,0]
        t[0]=i[1]
        r[i[0]]=t
    for i in res:
        if i[0] in r:
            r[i[0]][1]=i[1]
    for k,v in r.items():
        x.append(k)
        x1.append(k)
        y.append(v[0])
        y1.append(v[1])
    bar=Bar("排名前九用户消费额与购物次数柱状图","用户名","数值")
    bar.make(x,y,label="消费额",width=0.5)
    bar.make(x1,y1,label="购物次数",facecolor="green",width=0.5)
    bar.show()

t1()
t2()
t3()
t4()
t5()
t6()
t7()