#coding=utf-8
import json
import models
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """各类目发帖量统计 柱状图"""
    pipeline = [
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
    ]

    result = models.pipeline_select(pipeline)
    series = []
    for i in result:
        info = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': 'column'
        }
        series.append(info)
    context = {
        'series':series
    }
    return render(request, "htmls/home.html", context)

def pie(request):
    """一天内交易物品的种类分布，饼状图"""
    #一天内交易物品种类分布
    pipeline = [
        {'$match': {'time': 1}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    #一天内交易物品地区分布
    pipeline2 = [
        {'$match':{'time':1}},
        {'$group':{'_id':{'$slice':['$area',1]},'counts':{'$sum':1}}},
        {'$sort':{'counts':-1}}
    ]
    result_cate = models.pipeline_select(pipeline)
    data_cate = [{'name': i['_id'][0], 'counts': i['counts']} for i in result_cate]
    title_cate = '一天内交易物品种类分布'

    result_area = models.pipeline_select(pipeline2)
    data_area = [{'name': i['_id'][0], 'counts': i['counts']} for i in result_area]
    title_area = '一天内交易物品地区分布'
    context = {
        'data_cate':data_cate,
        'title_cate':title_cate,
        'data_area':data_area,
        'title_area':title_area
    }

    return render(request,'htmls/pie.html',context)

def top3(request):
    """各地区交易量TOP3的类目"""
    #查询所有的地区
    pipeline_area = [
        {'$group':{'_id':{'$slice':['$area',1]}}}
    ]
    result_area = models.pipeline_select(pipeline_area)
    areas = [i['_id'][0] for i in result_area]

    area = areas[0]
    #查询地区热门top3交易类目
    pipeline = [
        {'$match':{'area':area}},
        {'$group':{'_id':{'$slice':['$cates',2,1]},'counts':{'$sum':1}}},
        {'$sort':{'counts':-1}},
        {'$limit':3}
    ]

    result = models.pipeline_select(pipeline)
    top3_info = [{'name':info['_id'][0],'counts':info['counts']} for info in result]
    context = {
        'areas':areas,
        'top3_info':top3_info,
        'title':area
    }
    return render(request,'htmls/top3.html',context)

def yibu(request):
    """接收ajax请求，并返回地区交易量TOP3的类目 的json格式数据"""
    area = request.GET.get('area')
    pipeline = [
        {'$match': {'area': area}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}},
        {'$limit': 3}
    ]

    result = models.pipeline_select(pipeline)
    top3_info = [{'name': info['_id'][0], 'counts': info['counts']} for info in result]
    context = {
        'top3_info': top3_info,
        'title': area
    }
    return HttpResponse(json.dumps(context),content_type='application/json')

def base(request):
    return render(request,'htmls/base.html')


