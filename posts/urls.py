from django.conf.urls import url
from posts.views import UserPostViewSet, ClassroomPostViewSet, CommentViewSet

urlpatterns = [
    url(r'^users/(?P<user_id>\d+)/posts/$', UserPostViewSet.as_view({'get': 'list'}), name='user-post-list'),
    url(r'^classrooms/(?P<classroom_id>\d+)/posts/$', ClassroomPostViewSet.as_view({'post': 'create'}), name='classroom-post-list'),
    url(r'^classrooms/(?P<classroom_id>\d+)/posts/(?P<post_id>\d+)/$', ClassroomPostViewSet.as_view({'get': 'retrieve'}), name='classroom-post-detail'),
    url(r'^classrooms/(?P<classroom_id>\d+)/posts/(?P<post_id>\d+)/comments/$', CommentViewSet.as_view({'post': 'create'}), name='post-comment-list'),
]
