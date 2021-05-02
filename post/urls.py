from django.urls import re_path

from post.views import PostViewSet


post_list = PostViewSet.as_view({
    'post': 'post',
    'get': 'list'
})

post_detail = PostViewSet.as_view({
    'get': 'get_post',
    'put': 'edit_post',
    'delete': 'delete_post'
})

urlpatterns = [
    re_path(r'^/?$', post_list, name='post-list'),
    re_path(r'^/(?P<pk>\d+)/?$', post_detail, name='post-detail'),
    re_path(r'^/search/?$', PostViewSet.as_view({'get': 'search'}), name='search'),
]
