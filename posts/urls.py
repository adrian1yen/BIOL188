from django.conf.urls import url
from posts.views import PostViewSet

urlpatterns = [
    url(r'^posts/$', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
]
