import base64
import json
import re
import os
import jieba
import random
from datetime import datetime
from io import BytesIO
from django.shortcuts import render
from chatgptcomments.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from simtext import similarity


# Create your views here.
def showIndex(request):
    comments = Comments.objects.order_by('?')[:100]
    paginator = Paginator(comments, 10)
    page = request.GET.get('page')
    data_list = []
    if page:
        data_list = paginator.page(page).object_list
    else:
        data_list = paginator.page(1).object_list
    try:
        page_object = paginator.page(page)
    except PageNotAnInteger:
        page_object = paginator.page(1)
    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)
    return render(request, "index.html", {
        'page_object': page_object,
        'data_list': data_list
    })


# 定义关键词检索请求链接.
def searchindex(request):
    res = {
        'status': 404,
        'text': 'Unknown request!'
    }
    print(request)
    if request.method == 'GET':
        name = request.GET['id']
        if name == 'submit2search':
            try:
                # 获取前端的关键词
                keyword = request.GET['keyword']
                print(keyword)
                # 精确匹配索引关键词
                invertedindex_rec = CommentIndex.objects.get(cmt_keyword=keyword)
                # 将文档列表字符串转化成数组
                jsonDec = json.decoder.JSONDecoder()
                result = jsonDec.decode(invertedindex_rec.cmt_list)
                result_queryset = Comments.objects.filter(id__in=result).values()
                result_ls = list(result_queryset)
                if result_queryset:
                    res = {
                        'status': 200,
                        'text': result_ls,
                    }
                else:
                    res = {
                        'status': 201,
                        'text': 'No result!',
                    }
            except ObjectDoesNotExist:
                res = {
                    'status': 201,
                    'text': 'No result!',
                }
    return HttpResponse(json.dumps(res), content_type='application/json')


# 定义文本检索请求链接.
# def textsearch(request):
#     res = {
#         'status': 404,
#         'text': 'Unknown request!'
#     }
#     if request.method == 'GET':
#         name = request.GET['id']
#         if name == 'text2search':
#             try:
#                 # 获取前端的关键词
#                 text = request.GET['text']
#                 cmts_list = Comments.objects.order_by('?').values('content')[:1000]
#                 ret = {}
#                 for cmt in cmts_list:
#                     cmt = cmt['content']
#                     # 对句子进行分词，并添加特殊标记
#                     sim = similarity()
#                     res = sim.compute(cmt, text)
#                     ret[cmt] = res['Sim_Cosine']
#
#                 ret = sorted(ret.items(), key=lambda d: d[1], reverse=True)
#                 result_ls = []
#                 for i in range(20):
#                     result_ls.append(ret[i][0])
#                 print(result_ls)
#                 if len(result_ls) > 0:
#                     res = {
#                         'status': 200,
#                         'text': result_ls,
#                     }
#                 else:
#                     res = {
#                         'status': 201,
#                         'text': 'No result!',
#                     }
#             except ObjectDoesNotExist:
#                 res = {
#                     'status': 201,
#                     'text': 'No result!',
#                 }
#     return HttpResponse(json.dumps(res), content_type='application/json')


def showAnalysis(request):
    img_with_text_list = CommentView.objects.all()
    cluster = {}
    sentiment = {}
    for img_with_text in img_with_text_list:
        url = img_with_text.img_name
        img_root = "/static/images/"
        root_dir = url.split('/')
        if root_dir[0] == "cluster":
            cluster[img_root + url] = img_with_text.img_text
        elif root_dir[0] == "sentiment":
            sentiment[img_root + url] = img_with_text.img_text
        else:
            print("路径名出错了")
    return render(request, 'analysis.html', {
        'cluster': cluster,
        'sentiment': sentiment
    })


def showSearch(request):
    result_ls = []
    text = 'No result'
    if request.method == 'GET':
        # 获取前端的关键词
        text = request.GET['text']
        cmts_list = Comments.objects.order_by('?').values('content')[:1000]
        ret = {}
        for cmt in cmts_list:
            cmt = cmt['content']
            # 对句子进行分词，并添加特殊标记
            sim = similarity()
            res = sim.compute(cmt, text)
            ret[cmt] = res['Sim_Cosine']
        ret = sorted(ret.items(), key=lambda d: d[1], reverse=True)
        for i in range(20):
            result_ls.append(ret[i][0])
    return render(request, 'search.html', {
        "result_ls": result_ls,
        "header": text
    })


def showQAchat(request):
    return render(request, 'qachat.html')


# 定义问题请求，获取回答
@csrf_exempt
def getAnswering(request):
    res = {
        'status': 404,
        'content': 'Unknown request!'
    }
    print(request)
    if request.method == 'POST':
        question = request.POST['prompt']
        try:
            answer = QAchatMethod(question)
            res = {
                'status': 200,
                'content': answer
            }
        except:
            res = {
                'status': 201,
                'content': 'No result!'
            }
    return HttpResponse(json.dumps(res), content_type='application/json')


def get_matchingids(question):
    matching_ids = set()  # 初始化匹配 ID 的集合
    id_num = {}  # 初始化匹配关键词的对应id和数量的空字典
    index_reader = QAIndex.objects.all()
    for row in index_reader:
        keyword = row.keyword
        ids = set(row.ids.split(','))  # 将 IDs 转换为集合类型
        # 使用jieba进行中文分词
        question_words = jieba.lcut(question)
        # 找到匹配的索引词对应的id，写入字典中，并统计数量
        if any(word in keyword for word in question_words):
            # print('1')
            # print(matching_ids)
            for id in ids:
                if id not in id_num:
                    id_num[id] = 1
                else:
                    id_num[id] = id_num[id] + 1
    # 排序并记录数量最多的索引
    sort_id_num = sorted(id_num.items(), key=lambda x: x[1], reverse=True)
    max_num = 0
    # print(sort_id_num)
    for item in sort_id_num:
        if item[1] >= max_num:
            max_num = item[1]
            matching_ids.add(item[0])
        if item[1] < max_num:
            break
    # print(matching_ids)
    if len(matching_ids) == 0:
        return -1
    return matching_ids


def QAchatMethod(question):
    # 读取分词索引 CSV 文件
    matching_ids = get_matchingids(question)
    if matching_ids == -1:
        return "对不起，我无法回答这个问题"
    # 随机选择一个匹配的 ID
    selected_id = int(random.choice(list(matching_ids)))

    # 读取问答数据 CSV 文件
    qa_reader = QAmap.objects.all()
    # 查找选定的 ID 对应的答案
    for row in qa_reader:
        if row.id == selected_id:
            return row.answer
    return "对不起，找不到相关答案。"


def showHelp(request):
    return render(request, 'template.html')
