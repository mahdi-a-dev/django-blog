from django.shortcuts import get_object_or_404

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from .forms import PostCreationForm, CommentForm

from .models import Post, Category, Comment


# ---------------- POST ----------------


class PostList(ListView):
    """
    Display a list of Posts Where status is True
    """
    queryset = Post.objects.filter(status=True)
    context_object_name = "posts"
    paginate_by = 4


class PostDetail(DetailView):
    """
    Display a single Post details
    """ 
    model = Post
    context_object_name = "post"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    """
    Display a Post creation form,
    only authenticatec user can access.
    """
    model = Post
    form_class = PostCreationForm
    success_url = reverse_lazy("blog:post-list")
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Create Post"
        
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UpdateView):
    """
    Display a Post Update form,
    only authenticatec user can access.
    """
    model = Post
    form_class = PostCreationForm
    success_url = reverse_lazy("blog:post-list")
    
    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user.profile
        )
        

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Update Post"
        
        return context


class DeletePost(LoginRequiredMixin, DeleteView):
    """
    Display a Post confirm delete form,
    only authenticatec user can access.
    """
    model = Post
    success_url = reverse_lazy("blog:post-list")
    
    
    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user.profile
        )


# ---------------- COMMENT ----------------


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    
    
    def get_post(self):
        return get_object_or_404(
            Post,
            pk=self.kwargs["post_id"]
        )


    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.instance.post = self.get_post()
        
        return super().form_valid(form)

    def get_success_url(self):
        
        return reverse(
            "blog:post-detail",
            kwargs={"pk": self.kwargs["post_id"]}
        )


class EditComment(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/edit-comment.html"
      

    def get_queryset(self):
        return Comment.objects.filter(
            profile__user=self.request.user,
            post__id=self.kwargs["post_id"]
        )


    def get_success_url(self):
        return reverse(
            "blog:post-detail",
            kwargs={"pk": self.kwargs["post_id"]}
        )


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Post
    
    def get_queryset(self):
        return Comment.objects.filter(
            profile__user=self.request.user,
            post__id=self.kwargs["post_id"]
        )
    
    def get_success_url(self):
        return reverse(
            "blog:post-detail",
            kwargs={"pk": self.kwargs["post_id"]}
        )