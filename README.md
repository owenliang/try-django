# django官方教程（精简+注释版）

## 安装

记住用python3.5+。

```
pip3 install django
```

## 创建项目

每个项目对应一个域名。

```
django-admin startproject mysite
```

## 创建应用

每个应用对应一个子功能集合, 比如：user用户、order订单、goods商品。

在什么目录执行都可以, django会根据manage.py文件所在目录相对创建user子目录

```
python3 manage.py user
```

## 实现接口

编辑user/views.py

```
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello world')
```

## 配置子路由

新建user/urls.py, 采用相对导入可以降低心智负担。

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
]
```

## 配置全局路由

修改mysite/urls.py, 当访问/user对应子路由user.urls模块。

django会通过__import__动态完成user.urls的类加载, 我们需要书写以manage.py同级的包名。

这是因为python manage.py时会在sys.path中加入其所在目录作为包查找路径。

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls),
]
```

## 运行框架

运行，访问http://127.0.0.1:8000/user

```
python3 manage.py runserver
```

## 安装mysqlclient

为了访问mysql，在mac环境下进行如下操作：

```
brew install openssl
sudo LDFLAGS="-L/usr/local/opt/openssl/lib" pip3 install mysqlclient
```

## 创建数据库

在mysql中执行：

```
create database mysite
```

## 配置数据库

编辑mysite/settings.py：

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',
        'USER': 'root',
        'PASSWORD': 'baidu@123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

## 修改时区

编译mysite/settings.py，令其使用操作系统配置的时区：

```
USE_TZ = False
```

## 初始化内置APP数据库

虽然这些功能不一定都用到, 但都做一下吧:

```
python3 manage.py migrate
```

产生了一些表：

```
mysql> use mysite;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+----------------------------+
| Tables_in_mysite           |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+
10 rows in set (0.00 sec)
```

## 创建model

model有2个用途, 一个是ORM操作数据库，一个是校验数据。

CharField(max_length=32)对应数据库varchar(32)：

```
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=32)
    passwd = models.CharField(max_length = 32)
    create_date = models.DateTimeField()
```

## 创建表

默认model访问的表名是: "app名_model名"，所以创建一个表如下：

```
CREATE TABLE `user_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `passwd` varchar(32) NOT NULL,
  `nickname` varchar(64) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY name (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

## 定义接口

编辑user/views.py，定义5个增删改查接口：

```
from django.http import HttpResponse

# 列表
def index(request):
    return HttpResponse('detail')
    
# 获取用户
def detail(request):
    return HttpResponse('detail')

# 新建用户
def create(request):
    return HttpResponse('create')

# 更新用户
def update(request):
    return HttpResponse('update')

# 删除
def delete(request):
    return HttpResponse('delete')

```

## 配置路由

编辑user/urls.py，配置app的路由命名空间，以及路由项：

```
from django.urls import path
from . import views

# 路由的命名空间, 必须叫app_name
app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('detail', views.detail, name='detail'),
    path('update', views.update, name='update'),
    path('delete', views.delete, name='delete')
]
```

每个path项都有一个name标示，为了和其他app下的同名name做区分，django支持通过app_name变量指定路由的命名空间。

具体app_name和name怎么用，后面会提到。

## 注册应用

为了顺利加载user app下面的模板文件，需要注册app。

编辑mysite/settings.py：

```
INSTALLED_APPS = [
    'user.apps.UserConfig', # 这里把user.apps模块的UserConfig类注册上来, 类中的name属性标识了app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

像django这种框架的各种配置化功能，最终都是基于__import__动态加载模块实现的，没有什么神奇的。


## 编写模板

创建user/templates目录，因为我们注册了user应用，后续框架也会在该目录下进行模板文件的查找（框架也会扫描其他app）。

模板文件类似于路由，因为框架是无脑扫描所有app目录的，所以在某个app内也需要用目录命名空间去划分（避免和其他app冲突），所以应该创建user/templates/user/index.html：

```
{% include 'user/header.html' %}
<body>
    <form action="{% url 'user:create' %}" method="get">
        <input name="name" type="text">
        <input name="passwd" type="password">
        <input name="nickname" type="nickname">
        <input type="submit" value="保存">
    </form>
{% include 'user/footer.html' %}
```

这个表单是为了添加user用的。

其中url 'user:create'，user表示使用app_name='user'的urls.py，create表示使用path(name='create')的路由项，实际整体就是替换成对应的URI了。

然后创建user/templates/user/header.html：

```
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
    <link rel="stylesheet" type="text/css" href="{% static 'user/style.css' %}?ver=1">
</head>

```

用了static指令，它会补全URI为/static/user/style.css。

和路由/模板文件的查找规则一样，django会在所有app的static目录中查找这个名字，因此我需要将它放置在：

```
mysite/user/static/user/style.css
```

同样看一下footer.html：

```
</body>
</html>
```

# 渲染列表页

编辑user/views.py：

```
# 列表
def index(request):
    return render(request, 'user/index.html', {'title': '用户列表'})
```

django会去所有app的templates目录中查找user/index.html，并将第3个参数传入到模板。

# 实现保存接口

编辑user/views.py：

```
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
```

request.GET/POST[]获取参数如果不存在会抛异常，如果检查参数空返回400应答。

最终对model赋值，保存到数据库，并重定向页面到/user/index页。

# 完善列表页

编辑user/templates/index.html：

```
{% include 'user/header.html' %}
<body>
    <form action="{% url 'user:create' %}" method="get">
        <input name="name" type="text">
        <input name="passwd" type="password">
        <input name="nickname" type="nickname">
        <input type="submit" value="保存">
    </form>
    <table>
        <tr>
            <td>帐号</td>
            <td>密码</td>
            <td>昵称</td>
            <td>创建日期</td>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.passwd }}</td>
            <td>{{ user.nickname }}</td>
            <td>{{ user.create_date }}</td>
        </tr>
        {% endfor %}
    </table>
{% include 'user/footer.html' %}

```

编辑user/views.py，读取所有用户传给模板：

```
# 列表
def index(request):
    users = models.User.objects.all().order_by('-create_date')
    for user in users:
        user.create_date = user.create_date.strftime("%Y-%m-%d %H:%M:%S")

    return render(request, 'user/index.html', {'users': users, 'title': '用户列表'})
```

## 支持翻页

编辑user/views.py，支持简单的前后翻页：

```
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
```

然后在模板中展现超链接：

```
{% include 'user/header.html' %}
<body>
    <form action="{% url 'user:create' %}" method="get">
        <input name="name" type="text">
        <input name="passwd" type="password">
        <input name="nickname" type="nickname">
        <input type="submit" value="保存">
    </form>
    <table>
        <tr>
            <td>帐号</td>
            <td>密码</td>
            <td>昵称</td>
            <td>创建日期</td>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.passwd }}</td>
            <td>{{ user.nickname }}</td>
            <td>{{ user.create_date }}</td>
        </tr>
        {% endfor %}
    </table>
    {% if pagination.prev %}
        <a href="{% url 'user:index' %}?page={{pagination.prev}}">上一页</a>
    {% endif %}
   {% if pagination.next %}
        <a href="{% url 'user:index' %}?page={{pagination.next}}">下一页</a>
    {% endif %}
{% include 'user/footer.html' %}
```

## CURD之READ

编辑user/views.py:

```
# 获取用户
def detail(request):
    id = request.GET['id']

    user = models.User.objects.filter(id=id).get()

    user_dict = model_to_dict(user)
    user_dict['create_date'] = user_dict['create_date'].strftime('%Y-%m-%d %H:%M:%S')

    return HttpResponse(json.dumps(user_dict))
```

利用filter/exclude进行where条件的拼接，最后调get获取单条记录。

特殊的就是model中的datetime字段是date类型，需要手动转成字符串。


## CURD之UPDATE

编辑user/views.py:

```
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
```

request.GET.get('field', 'default value')允许默认值，客户端不传参也不会抛异常。

更新可以直接走update()方法，等价于数据库的update命令。

## CURD之DELETE

编译user/views.py：

```
# 删除
def delete(request):
    id = request.GET['id']

    models.User.objects.filter(id = id).delete()

    return HttpResponse('delete')
```

删除也可以通过[offset,limit]实现limit x,y的效果。

## 后续

根据个人感受，应该需要创建一个叫做common的app，在其中放置公用的templates/static/models/library等，作为其他app的公共代码存放地。

后续还要看看这些：

* session的用法
* cache的用法
