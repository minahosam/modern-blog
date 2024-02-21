from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('',home,name='home'),
    path('search/',search_posts,name='search'),
    path('<str:slug>/',post_detail,name='post_detail'),
    path('tag/<slug>/',tag_detail,name='tag_detail'),
    path('author/<slug>/',profile_page,name='author_detail'),
]
