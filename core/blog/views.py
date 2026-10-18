from django.shortcuts import redirect, get_object_or_404

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment

from django.utils import timezone

from django.db.models import Q


# ---------------- post views ----------------


class PostList(ListView):
    """
    Display a list of Posts Where status is True
    """
    context_object_name = "posts"
    paginate_by = 9
    template_name = "blog/post/post_list.html"
    
    def get_queryset(self):
        search_query = self.request.GET.get("s")
        
        posts = Post.objects.filter(status=True)
        
        if search_query:
            return posts.filter(
                Q(title__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        return Post.objects.filter(status=True)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        
        return context



class PostDetail(DetailView):
    """
    Display a single Post details
    """ 
    model = Post
    context_object_name = "post"
    template_name = "blog/post/post_detail.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_superuser:
            return queryset
        
        if user.is_authenticated:
            return queryset.filter(
                Q(status=True) |
                Q(author__user=user)
            )
            
        return queryset.filter(status=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        
        return context


class CreatePost(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Display a Post creation form,
    only authenticatec user can access.
    """
    model = Post
    form_class = PostForm
    template_name = "blog/post/post_form.html"
    success_url = reverse_lazy("accounts:profile")
    success_message = "Post created successfully."
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Create Post"
        
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Display a Post Update form,
    only authenticatec user can access.
    """
    model = Post
    form_class = PostForm
    template_name = "blog/post/post_form.html"
    success_url = reverse_lazy("accounts:profile")
    success_message = "Post updated successfully."
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        
        return Post.objects.filter(
            author=self.request.user.profile
        )
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Update Post"
        
        return context

    def test_func(self):
        return self.request.user.is_staff
        
class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Display a Post confirm delete form,
    only authenticatec user can access.
    """
    model = Post
    template_name = "blog/post/post_confirm_delete.html"
    success_url = reverse_lazy("accounts:profile")
    
    def form_valid(self, form):
        messages.success(self.request, "Post deleted successfully.")
        
        return super().form_valid(form)
 
    def test_func(self):
        return self.request.user.is_superuser


class ChangeStatusPost(LoginRequiredMixin, UserPassesTestMixin, View):
        
    def test_func(self):
        return self.request.user.is_superuser
    
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            pk=kwargs["pk"]
        )
        
        post.status = not post.status
        post.published_date = (
            timezone.now() if post.status else None
            )
        
        post.save(update_fields=["status", "published_date"])
        
        return redirect("accounts:profile")
        
# ---------------- category views ----------------

class CategoryPostList(ListView):
    model = Post
    template_name = "blog/category/category_posts.html"
    context_object_name = "posts"
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs["slug"]
        )
        
        return self.category.posts.filter(status=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
    

# ---------------- comments views ----------------


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
    template_name = "blog/comment/edit-comment.html"
      

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
    model = Comment
    template_name = "blog/comment/comment_confirm_delete.html"

    
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
