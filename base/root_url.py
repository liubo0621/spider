# encoding=utf8
import sys
sys.path.append("..")

import threading
import fileinput
import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.getConnectedDB()

class AddRootUrl(threading.Thread):
    _addUrlFuncs = []

    def __init__(self):
        super(AddRootUrl, self).__init__()

    def run(self):
        website = tools.getConfValue("collector", "website")
        self.registUrlFunc()

        # 执行add url func
        for addUrlFunc in AddRootUrl._addUrlFuncs:
            addWebUrl = addUrlFunc[0]
            domain = addUrlFunc[1]

            if website == 'all':
                addWebUrl()
            elif website == domain:
                addWebUrl()

    def addUrl(self, url, websiteId, description = '', depth = 0, status = Constance.TODO):
        for i in db.urls.find({'url':url}):
            return

        urlDict = {'url':url, 'description':description, 'website_id':websiteId, 'depth':depth, 'status':Constance.TODO}
        db.urls.save(urlDict)

    # 注册添加url的方法
    def registUrlFunc(self):
        AddRootUrl._addUrlFuncs.append([self.addLuZhou, Constance.LU_ZHOU])

    # 添加凤凰url
    def addLuZhou(self):
        baseUrl = "http://v.lzep.cn/"
        websiteId = tools.getWebsiteId(Constance.LU_ZHOU)
        self.addUrl(baseUrl, websiteId)