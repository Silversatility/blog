from django.urls import path
from .views import PostListView, PostDetailView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add-comment'),
]