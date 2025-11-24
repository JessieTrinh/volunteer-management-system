from django.urls import path
from .views import PostListView, PostEditView, PostDeleteView
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]