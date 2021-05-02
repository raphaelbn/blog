from django.urls import re_path

from user.views import LoginViewSet, UserViewSet


user_detail = UserViewSet.as_view({
    'post': 'post',
    'get': 'list'
})

urlpatterns = [
    re_path(r'^/?$', user_detail, name='user-detail'),
    re_path(r'^/(?P<pk>\d+)/?$', UserViewSet.as_view({'get': 'get'}), name='get'),
    re_path(r'^/me/?$', UserViewSet.as_view({'delete': 'delete'}), name='delete'),
    re_path(r'^/login/?$', LoginViewSet.as_view({'post': 'login'}), name='login'),
]
