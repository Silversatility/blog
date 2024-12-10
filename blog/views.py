from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    queryset = Post.objects.filter(status='published').select_related('author').order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created')
        context['comment_form'] = CommentForm() 
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_create.html'
    success_url = reverse_lazy('post-list') 

    def form_valid(self, form):
        post_id = self.kwargs.get('pk')
        form.instance.post = get_object_or_404(Post, pk=post_id)
        return super().form_valid(form)