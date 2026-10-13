from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileForm
from blog.models import Post
from .models import Profile


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("blog:post-list")


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("blog:post-list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("blog:post-list")
        return super(RegisterView, self).get(*args, **kwargs)
    

class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context["my_posts"] = Post.objects.filter(author=self.request.user.profile)
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "accounts/edit-profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("accounts:profile")
    
    def get_object(self):
        return get_object_or_404(
            Profile,
            user=self.request.user
        ) 

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Update Profile"
        
        return context

    
    
