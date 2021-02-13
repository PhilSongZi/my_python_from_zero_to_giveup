# 信息：排名 书名 图书地址 作者 推荐指数 五星评分次数 价格

# 1.网页分析：信息放在li标签中
# pic "http://img3m1.ddimg.cn/66/36/28470981-1_l_3.jpg
# name 谜案鉴赏
# star level 46974条评论 / tuijian 100%推荐
# publisher_info
# biaosheng 五星评分： 45119次
# price -->price_n 21.80

# 2.思路
# page变量实现翻页，requests请求网页，返回HTML用re解析，存文件
# 定义三个函数封装功能，一个main实现

import requests
import re
import json


def request_dangdang(url):
    """请求网页"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_request(html):
    """页面分析、数据提取"""
    # re表达式重中之重！！！
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        # yield生成器 真滴好用
        yield {
            "range": item[0],
            "image": item[1],
            "title": item[2],
            "recommend": item[3],
            "author": item[4],
            "times": item[5],
            "price": item[6]
        }
        print(item)


def write_item_to_file(item):
    """文件写入"""
    print("开始写入数据==>" + str(item))
    with open("../book.txt", "a", encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
        f.close()


def main(page):
    """main"""
    url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-" + str(page)
    html = request_dangdang(url)
    items = parse_request(html)

    # for item in items:
    #     print(item)

    for item in items:
        write_item_to_file(item)


if __name__ == "__main__":
    for i in range(1, 26):
        main(i)
