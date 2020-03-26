# print('my first py program')

# 1、引入需要要的包  
# 网络请求相关的包
from urllib.request import urlopen, Request
import ssl
# 正则相关的包
import re

# 配置https请求
ssl._create_default_https_context = ssl._create_unverified_context 
# 设置数据源地址
source_url = 'https://movie.douban.com/top250'
# 自定义http request请求头，豆瓣默认只允许部分UA进行访问 这里自定义User-Agent成浏览器的UA
custom_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
# 初始化Request
movie_request = Request(source_url, headers = custom_headers)
# 发出request请求
movie_response = urlopen(movie_request)
# 将读取结果进行utf-8解码，避免乱码
html = movie_response.read().decode('utf-8')
# 测试打印结果        
print(html)

# 定义一个函数，获取所有跟电影相关的<li></li>
def getMovieItems(content):
    # 匹配正则表达式 [\s\n]*表示，在<li>标签和<div之前可能会有多个空格(\s)或者换行符(回车或\n)  .*表示 除换行符以外的字符可能多次重复 ?表示匹配0个或1个由前面的正则表达式定义的片段
    reg = '<li>[\s\n]*<div.*?</li>'
    # 生成一个正则表达式对象 re.S表示 使 .匹配包括换行在内的所有字符
    item_wrap = re.compile(reg, re.S)
    print(item_wrap)
    # 在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表
    movie_items = re.findall(item_wrap, html)
    return movie_items

# 将从源网址获取到的结果进行匹配
movies = getMovieItems(html)
# 打印匹配结果 len()表示数组长度
print(movies, len(movies))

# 定义一个列表，用来存最终数据
list = []
# 循环遍历
for m in movies:
    # 删除掉 &nbsp;   
    m = re.sub('&nbsp;', '', m)
    dic = {}
    # 评分
    reg = '<em class="">(.*)</em>'
    ranking = re.findall(re.compile(reg), m)
    print(ranking)
    dic['ranking'] = ranking[0]

    # title
    reg = '<span class="title">(.*)</span>'
    title = re.findall(re.compile(reg), m)
    print(title)
    dic['title'] = title[0]

    # orther_title
    reg = '<span class="other">(.*)</span>'
    orther_title = re.findall(re.compile(reg), m)
    print(orther_title)
    dic['orther_title'] = orther_title[0]

    # type_people  导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>   1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
    reg = r'<p class="">(.*?)</p>'
    type_people = re.findall(re.compile(reg, re.S), m)[0]
    # 删除掉 <br>;   
    type_people = re.sub('<br>', '', type_people)
    # 删除掉 回车/换行符;   
    type_people = re.sub('\n', '', type_people)
    # 删除掉 空格;   
    type_people = re.sub('\s', '', type_people)
    print('type_people', type_people)

    # director 导演 匹配导演: 与 主演之前的内容 有些可能没有主演的演字...
    reg = r'导演:(.*)主'
    director = re.findall(re.compile(reg, re.S), type_people)
    print(director)
    dic['director'] = director[0]

     # year 年份  匹配4位数字
    reg = r'\d+'
    year = re.findall(re.compile(reg), type_people)
    print(year)
    dic['year'] = year[0]

    # actors 主演 从主演: 开始 截取至 4位年份止
    reg = r'主演:(.*)\d{4}'
    director = re.findall(re.compile(reg), type_people)
    print(director)
    if (len(director)):
        dic['director'] = director[0]

    # region 国家  从4位年份+'/'截取至下一个'/'
    reg = r'\d{4}/(.*)/'
    region = re.findall(re.compile(reg), type_people)
    print(region)
    if (len(region)):
        dic['region'] = region[0]
    
    # type 类型
    reg = r'\d{4}/.*/(.*)'
    region = re.findall(re.compile(reg), type_people)
    print(region)
    if (len(region)):
        dic['region'] = region[0]

    # douban_href <a href="https://movie.douban.com/subject/1292052/" class="">
    reg = r'<a href="(.*?)">'
    douban_href = re.findall(re.compile(reg, re.S), m)
    print(douban_href)
    dic['douban_href'] = douban_href[0]

    # average_rating
    reg = '<span class="rating_num" .*>(.*?)</span>'
    average_rating = re.findall(re.compile(reg), m)
    print(average_rating)
    dic['average_rating'] = average_rating[0]

    # votes <span>1944072人评价</span>
    reg = '<span>(.*)人评价</span>'
    votes = re.findall(re.compile(reg), m)
    print(votes)
    dic['votes'] = votes[0]

    # short_quote <span class="inq">
    reg = '<span class="inq">(.*)</span>'
    short_quote = re.findall(re.compile(reg, re.S), m)
    print(short_quote)
    dic['short_quote'] = short_quote[0]
    list.append(dic)

print(list)

import json

# 将list转换成json对象 格式缩进4个空格 中文字符正常显示，不转换成ascii
json_str = json.dumps(list,  indent=4, ensure_ascii=False)
# 新建一个movie-douban-top250.json文件 w+表示打开一个文件，如果文件存在则将内容清空
json_file = open('movie-douban-top250.json', 'w+')
json_file.writelines(json_str)
