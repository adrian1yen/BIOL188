from django.conf.urls import url
from views import UserViewSet

urlpatterns = [
    url(r'^users/$', UserViewSet.as_view({'get': 'list', 'post': 'retrieve'}), name='user-list'),
    url(r'^me/$', UserViewSet.as_view({'get': 'me'}), name='me'),
]
