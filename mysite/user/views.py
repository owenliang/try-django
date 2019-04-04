from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from . import models
from django.forms.models import model_to_dict
from django.utils import timezone
from django.shortcuts import render
import hashlib
import json
from django.urls import reverse

# 列表
def index(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 5))

    offset = (page - 1) * size

    users = models.User.objects.all().order_by('-create_date')[offset: offset + size]
    for user in users:
        user.create_date = user.create_date.strftime("%Y-%m-%d %H:%M:%S")

    user_count = models.User.objects.count()

    pagination = {}
    if page > 1:
        pagination['prev'] = page - 1
    if offset + len(users) < user_count:
        pagination['next'] = page + 1

    return render(request, 'user/index.html', {'users': users, 'title': '用户列表', 'pagination': pagination})

# 获取用户
def detail(request):
    id = request.GET['id']

    user = models.User.objects.filter(id=id).get()

    user_dict = model_to_dict(user)
    user_dict['create_date'] = user_dict['create_date'].strftime('%Y-%m-%d %H:%M:%S')

    return HttpResponse(json.dumps(user_dict))

# 新建用户
def create(request):
    # 取表单
    name = request.GET['name']
    passwd = request.GET['passwd']
    nickname = request.GET['nickname']

    # 返回异常应答
    if not name or not passwd:
        return HttpResponseBadRequest()

    md5 = hashlib.md5()
    md5.update(passwd.encode('utf-8'))

    # 保存
    user = models.User()
    user.name = name
    user.passwd = md5.hexdigest()
    user.nickname = nickname
    user.create_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    user.save()

    # 重定向回列表页
    return HttpResponseRedirect(reverse('user:index'))

# 更新用户
def update(request):
    id = request.GET['id']
    passwd = request.GET.get('passwd')
    nickname = request.GET.get('nickname')

    fields = {}
    if passwd:
        md5 = hashlib.md5()
        md5.update(passwd.encode('utf-8'))
        fields['passwd'] = md5.hexdigest()
    if nickname:
        fields['nickname'] = nickname

    models.User.objects.filter(id=id).update(**fields)

    return HttpResponse('update')

# 删除
def delete(request):
    id = request.GET['id']

    models.User.objects.filter(id = id).delete()

    return HttpResponse('delete')
