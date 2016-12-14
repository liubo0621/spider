
# encoding=utf8
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

DEBUG = False

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    sourceUrl = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    html = tools.getHtml(sourceUrl)
    if not DEBUG:
        if html == None:
            basePaser.updateUrl(sourceUrl, Constance.EXCEPTION)
            return

        # 取当前页面的全部url
        urls = tools.getUrls(html)

        # 只要包含关键字的url 添加到数据库
        fitUrl = tools.fitUrl(urls, 'v.lzep.cn')
        for url in fitUrl:
            # log.debug('url = ' + url)
            basePaser.addUrl(url, websiteId, depth + 1)


    # 取当前页的文章信息
    # 标题
    regexs = '<h1.*?>(.*?)</h1>'
    title = tools.getInfo(html, regexs)
    title = title and title[0] or ''
    title = tools.delHtmlTag(title)

    # 简介
    regexs = '<div class="digest">.*?简介：(.*?)</p>'
    abstract = tools.getInfo(html, regexs)
    abstract = abstract and abstract[0] or ''
    abstract = tools.delHtmlTag(abstract)

    # 发布时间
    regex = '<span class="date f-l">(.*?)</span>'
    releaseTime = tools.getInfo(html, regex)
    releaseTime = ''.join(releaseTime)

    #来源
    regex = '来源:(.*?) '
    origin = tools.getInfo(html, regex)
    origin = ''.join(origin)

    # 责任编辑 editor
    regex = '责任编辑：(.*?)</p>'
    editor = tools.getInfo(html, regex)
    editor = ''.join(editor)

    # 页面url
    pageUrl = sourceUrl

    # 视频url
    regexs = 'var flashvars={f:\'(.*?)\''
    videoUrl = tools.getInfo(html, regexs)
    videoUrl = ''.join(videoUrl)

    log.debug('''
        pageUrl:      %s
        videoUrl:     %s
        title:        %s
        abstract:     %s
        releaseTime:  %s
        origin:       %s
        editor:       %s
        depth:        %d
        '''%(pageUrl, videoUrl, title, abstract, releaseTime, origin, editor, depth))


    if not DEBUG:
        if videoUrl:
            basePaser.addVideoInfo(websiteId, pageUrl, videoUrl, title, abstract, releaseTime, origin, editor)

        # 更新sourceUrl为done
        basePaser.updateUrl(sourceUrl, Constance.DONE)

if __name__ == '__main__':
    DEBUG = True
    url = 'http://v.lzep.cn/2016/0805/200490.shtml'
    haha = {'url': url, 'website_id': '582ea577350b654b67dc8ac8', 'depth': 1, 'description': ''}
    parseUrl(haha)