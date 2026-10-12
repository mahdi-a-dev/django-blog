from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PostCreationForm
from .models import Post


class PostListView(ListView):
    """
    Display a list of Posts Where status is True
    """
    
    queryset = Post.objects.filter(status=True)
    context_object_name = "posts"
    paginate_by = 4


class PostDetailView(DetailView):
    """
    Display a single Post details
    """
    
    model = Post
    context_object_name = "post"


class CreatePostView(LoginRequiredMixin, CreateView):
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


class UpdatePostView(LoginRequiredMixin, UpdateView):
    """
    Display a Post Update form,
    only authenticatec user can access.
    """
    model = Post
    form_class = PostCreationForm
    success_url = reverse_lazy("blog:post-list")
    
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Update Post"
        
        return context



class DeletePostView(LoginRequiredMixin, DeleteView):
    """
    Display a Post confirm delete form,
    only authenticatec user can access.
    """
    model = Post
    success_url = reverse_lazy("blog:post-list")

    


