import requests
from bs4 import BeautifulSoup
import re
import pymysql
import pyhdfs

def create():
    db = pymysql.connect("172.17.0.2", "root", "abc123456", "news", charset='utf8') # 连接数据库

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS EMPLOYER")

    sql = """CREATE TABLE EMPLOYER (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            LOGO  CHAR(255),
            PRICE CHAR(20),
            AUTHER CHAR(255) )"""

    cursor.execute(sql)
    db.close()


def insert(value):
    db = pymysql.connect("172.17.0.2", "root", "abc123456", "news", charset='utf8')

    cursor = db.cursor()
    sql = "INSERT INTO EMPLOYER(LOGO,PRICE,AUTHER) VALUES (%s, %s,  %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()


create()  # 创建表

# re匹配需要的数据
pertern = re.compile(
    r'<img.*?data-original="(.*?)".*?<span class="search_now_price">(.*?)</span>.*?<a.*?单品作者.*?title="(.*?)">.*?</a>',
     )
# 添加请求头   修改user-agent来伪装浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
# url = 'http://category.dangdang.com/cp01.19.34.00.00.00.html'
url = 'http://category.dangdang.com/cp01.19.34.00.00.00-srsort_sale_amt_desc.html'
res = requests.get(url, headers=headers)
print(res.status_code)
soup = BeautifulSoup(res.text, 'html.parser')
data = soup.find_all('ul', attrs={'class': 'bigimg'})
data = str(data)
item = re.findall(pertern, data)
for i in item:
    print(i)
    insert(i)

    html = """<html>
<head></head>
<body>
<h1>当当网热门书籍检索</h1>
<ul>
"""
    for i in item:
        html += """<li><image src="""
        html += i[0]
        html += """">"""
        html += i[1]
        html += """></li>"""
        html +="""<li>"""
        html += i[2]
        html += """</li>"""
        # html += """<li>"""
        # html += i[3]
        # html += """</li>"""
    html += """</ul></body></html>"""
with open("206.html", "w", encoding="utf-8") as f:
    f.write(html)