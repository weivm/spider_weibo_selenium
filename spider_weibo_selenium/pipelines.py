# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WbSeleniumPipeline:
    def __init__(self):
        self.file = None
        self.writer = None

    def open_spider(self, spider):
        self.file = open('output.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

        # 写入表头，标识字段的意义
        self.writer.writerow(['链接', '热搜名', '热搜数量'])

    def close_spider(self, spider):
        if self.file:
            self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow([item['url'], item['name'], item['count']])
        return item