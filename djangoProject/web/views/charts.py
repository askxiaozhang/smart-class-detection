from django.shortcuts import render,redirect
from django import forms

from collections import namedtuple
from web import models

from web.utils.bootstrap import BootStrapModelForm
from django.http import JsonResponse #返回js数据

ChartName = namedtuple("ChartName",["name","url", "nick"])
chart_list = [
    ChartName("课堂不同状态随时间变化的状态统计折线图","chart_types_line", "课堂不同状态随时间变化的状态统计"),
    ChartName("折线图-电影年份分布","chart_types_yearsall2","电影年份分布"),
]

def chart_types_line(req):
    import random
    times = [i * 30 for i in range(1, 81)]
    listening_percentages = [random.randint(50, 100) for _ in range(len(times))]

    result = {
        "status": True,
        "data": {
            "listening_percentages": listening_percentages,
            "times": times
        }
    }

    return JsonResponse(result)