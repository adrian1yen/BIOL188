from django.conf.urls import url
from views import UserViewSet

urlpatterns = [
    url(r'^users/$', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    url(r'^users/(?P<userId>\d+)/$', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    url(r'^me/$', UserViewSet.as_view({'get': 'me'}), name='me'),
]
