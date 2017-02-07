#coding=utf-8

#models.py
from __future__ import unicode_literals
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ganji_db = client['ganji']
item_collection = ganji_db['item_info']

def pipeline_select(pipeline):
    """mongodb 管道查询"""
    return item_collection.aggregate(pipeline)
