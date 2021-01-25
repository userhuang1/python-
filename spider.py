from bs4 import BeautifulSoup as bf   #爬虫所需的主要的库
import re   #正则表达式
import urllib.request as web


work_name = []  # 岗位名称
area_name = []  # 工作地点
salary_name = []  # 薪水
edu_name = []  # 学历
experience_name = []  # 工作经验


def askURL(url):  # 访问某网址
    # url = "https://www.51job.com/"
    headers = {   #在network中寻找到 ，用来模拟游览器上网
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75"
    }
    req = web.Request(url=url, headers=headers)  # 实例化得到的对象
    response = web.urlopen(req)  # 爬的动作
    html = response.read().decode('gbk')  # 显示编码的格式，
    return html


def getdata(start,end,w):  #获取数据
    # datalist = []
    for i in range(1,30):  #这里是要爬取的页数
        url = start + str(i) + end   #根据i可以得出要爬取的网页网址
        html = askURL(url)   #对链接的访问
        soup = bf(html,'html.parser')  #解析HTML文件
        soup = str(soup)  #转为string类型，用于正则匹配
        reg = re.compile(r'window.__SEARCH_RESULT__ = .*?"engine_search_result":([\s\S]*?)</script>')  #正则表达式查找
        print(reg)  #可以用于查看获取的片段是什么样子的。
        # result = reg.findall(soup)[0]
        # print(result)
        result = reg.findall(soup)[0]  #直接取第一个
        # print(result)
        # print(type(result))
        cur = re.compile(r'"job_title":"(.*?)"',re.S)  #查找工作名称
        work_name = cur.findall(result)
        # print(work_name)
        cur = re.compile(r'"workarea_text":"(.*?)"',re.S)  #查找所在地区
        area_name = cur.findall(result)
        # print(area_name)
        cur = re.compile(r'providesalary_text":"(.*?)"', re.S)  # 查找所在地区
        salary_name = cur.findall(result)
        # print(salary_name)
        cur = re.compile(r'经验","(.*?)"', re.S)  # 查找所需学历
        edu_name = cur.findall(result)
        # print(edu_name)
        cur = re.compile(r'","(...?.?)经验', re.S)  # 查找所需工作经验
        experience_name = cur.findall(result)
        # print(experience_name)
        # print(len(work_name),len(area_name),len(salary_name),len(edu_name),len(experience_name))
        if(len(work_name) == len(area_name) == len(salary_name) == len(edu_name) == len(experience_name)): #将所有数据都满足的网址里的数据放入表格中
            w += 1
            save(w,work_name,area_name,salary_name,edu_name,experience_name)  #跳转函数

def save(i1,work_name,area_name,salary_name,edu_name,experience_name):  #存储数据到Excel表格中
    with open("data.xls",'a+',encoding='utf-8') as f:
        print(i1)
        if i1==1:   # 加入文件的首行
            f.write("职务")
            f.write('\t')
            f.write("地区")
            f.write('\t')
            f.write("薪水")
            f.write('\t')
            f.write("学历")
            f.write('\t')
            f.write("工作经验")
            f.write('\n')
        # print(len(work_name))
        for i in range(len(work_name)):   #分别加入每一行数据
            f.write(work_name[i])
            f.write('\t')
            f.write(area_name[i])
            f.write('\t')
            f.write(salary_name[i])
            f.write('\t')
            f.write(edu_name[i])
            f.write('\t')
            f.write(experience_name[i])
            f.write('\n')
    f.close()



if __name__ == '__main__':
    #51job的网址
    #start表示前面的，end表示后面的，
    start = 'https://search.51job.com/list/000000,000000,0000,00,9,99,java,2,'
    end = '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    getdata(start,end,0) #解析每一个网址


