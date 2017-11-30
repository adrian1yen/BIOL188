from django.conf.urls import url
from users.views import UserListViewSet, UserDetailViewSet, ClassroomDetailViewSet, ClassroomListViewSet

# User endpoints
urlpatterns = [
    url(r'^users/$', UserListViewSet.as_view({'post': 'create'}), name='user-list'),
    url(r'^users/(?P<user_id>\d+)/$', UserDetailViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    url(r'^me/$', UserDetailViewSet.as_view({'get': 'me'}), name='me'),
    url(r'^users/(?P<user_id>\d+)/add_class/$', UserDetailViewSet.as_view({'post': 'add_class'}), name='add-class'),
]

# Classrom endpoints
urlpatterns += [
    url(r'^classrooms/$', ClassroomListViewSet.as_view({'post': 'create'}), name='classroom-list'),
    url(r'^classrooms/(?P<classroom_id>\d+)/$', ClassroomDetailViewSet.as_view({'get': 'retrieve'}), name='classroom-detail'),
]
