# 分析网页：翻页start=25 ; 电影の——名称、图片、排名、评分、作者、简介
# rank  <em class="">1</em>
# img <img width="100" alt="肖申克的救赎" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" class="">
# title <span class="title">肖申克的救赎</span>
#       <span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>
#        <span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span>
# info  导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>
#        1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
# star -->rating_num 9.6
# quote  <span class="inq">希望让人自由。</span>


# 1.请求网页获得内容 2.分析内容bs4处理 3.存到excel 4.main

import requests
from bs4 import BeautifulSoup
import xlwt

url = "https://movie.douban.com/top250?start=1"


def request_douban(url):
    """获取网页源码"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


# 从这个试验 看出来好像是做了反爬措施鸭 咋办呀
# r = request_douban(url)
# print(r)
# response = requests.get(url)
# print(response.text)


# 建表
book = xlwt.Workbook(encoding="utf-8", style_compression=0)

sheet = book.add_sheet("豆瓣电影TOP250", cell_overwrite_ok=True)
sheet.write(0, 0, "名称")
sheet.write(0, 1, "图片")
sheet.write(0, 2, "排名")
sheet.write(n, 3, "评分")
sheet.write(0, 4, "作者")
sheet.write(0, 5, "简介")

n = 1


def save_to_excel(soup):
    """按照我这个写法不就成了我在这个spider里重写了beautifulsoup吗
    所以说应该是在main中bs4解析 在保存的函数中分类列出信息 再直接存下来"""

    list_str = soup.find(class_="grid_view").findall("li")

    for item in list_str:
        item_name = item.find(class_="title").string
        item_img = item.find("a").find("img").get("src")
        item_index = item.find(class_='').string
        item_score = item.find(class_="rating_num").string
        item_author = item.find("p").text
        item_instr = item.find(class_="inq").string

        print("爬取电影：" + item_index + "|" + item_name + "|" + item_score + "|" + item_instr)

        global n   # 声明全局
        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_instr)

        n += 1   #计数器自增 否则死循环


def main(page):
    url = "https://movie.douban.com/top250?start=" + str(page * 25)  #+ "&filter="
    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


if __name__ == "__main__":
    for i in range(0, 10):   # 因为start=25 一页25个 首页应为0开始
        main(i)

book.save(u"豆瓣最受欢迎的250部电影.xlsx")

