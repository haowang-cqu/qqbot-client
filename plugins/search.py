import requests
from lxml import etree 


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


def baidu(keywords: str, site: str = ""):
    """百度搜索
    """
    query = {
        'ie': 'UTF-8',
        'wd': f'{keywords} site:{site}'
    }
    resp = requests.get("https://www.baidu.com/s", params=query, headers=headers)
    if resp.status_code != 200:
        return None
    html = etree.HTML(resp.text, etree.HTMLParser())
    urls = html.xpath('//div[@id="content_left"]/div[@class="result c-container new-pmd"]/h3/a/@href')
    real_urls = []
    for url in urls:
        try:
            resp = requests.get(url)
        except Exception:
            continue
        else:
            real_urls.append(resp.url)
    return real_urls


def zhihu(keywords: str) -> str:
    """知乎问题
    """
    data = {
        'url': '',
        'title': keywords,
        'content': '',
        'image': 'https://pic2.zhimg.com/v2-dabccb1dd4014217316be5ea14021653_xll.jpg'
    }
    urls = baidu(keywords, "www.zhihu.com")
    for url in urls:
        data['url'] = url
        if url.startswith("https://www.zhihu.com/question/"):
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                html = etree.HTML(resp.text, etree.HTMLParser())
                # 获取标题
                titles = html.xpath('//div[contains(@class, "QuestionHeader-main")]//h1/text()')
                if len(titles):
                    data['title'] = titles[0]
                # 获取详情
                contents = html.xpath('//div[contains(@class, "QuestionRichText")]//text()')
                content = "".join(contents)
                if len(content) > 50:
                    data['content'] = content[:50]
                else:
                    data['content'] = content
                if len(data['content']) < 7:
                    contents = html.xpath('//div[contains(@class, "RichContent")]//text()')
                    content = "".join(contents)
                    # print(content)
                    if len(content) > 50:
                        data['content'] = content[:50]
                    else:
                        data['content'] = content
                # 获取图片
                images = html.xpath('//noscript/img/@src')
                if len(images):
                    data['image'] = images[0]
            return data
    return None

# print(zhihu("C++"))