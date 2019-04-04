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
