from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    # post list
    path("", views.PostListView.as_view(), name="post-list"),
    # post detail
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    # create
    path("post/create/", views.CreatePostView.as_view(), name="post-create"),
    # edit
    path("post/<int:pk>/edit/", views.UpdatePostView.as_view(), name="post-edit"),
    # delete
    path("post/<int:pk>/delete", views.DeletePostView.as_view(), name="post-delete"),
    
    # api
    path("api/", include("blog.api.urls"))
]
