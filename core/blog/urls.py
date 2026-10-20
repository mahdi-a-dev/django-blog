from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    # -------- post --------
    
    # post list
    path("", views.PostList.as_view(), name="post-list"),
    # post detail
    path("post/<int:pk>/", views.PostDetail.as_view(), name="post-detail"),
    # create, only staff users
    path("post/create/", views.CreatePost.as_view(), name="post-create"),
    # edit, only staff users
    path("post/<int:pk>/edit/", views.UpdatePost.as_view(), name="post-edit"),
    # delete, only superusers
    path("post/<int:pk>/delete", views.DeletePost.as_view(), name="post-delete"),
    # change status, only superusers
    path("post/<int:pk>/change_status", views.ChangeStatusPost.as_view(), name="post-change-status"),

    # -------- category --------
    
    path("category/<slug:slug>/", views.CategoryPostList.as_view(), name="category-posts"),
    
    # -------- comment --------
    
    # add, only authenticated users
    path("post/<int:post_id>/comment/add", views.AddComment.as_view(), name="add-comment"),
    # reply, only authenticated users
    path("post/<int:post_id>/comment/<int:pk>/reply", views.ReplyComment.as_view(), name="reply-comment"),
    # edit, only authenticated users
    path("post/<int:post_id>/comment/<int:pk>/edit", views.EditComment.as_view(), name="edit-comment"),
    # delete, only authenticated users
    path("post/<int:post_id>/comment/<int:pk>/delete", views.DeleteComment.as_view(), name="delete-comment"),
    
    # api
    path("api/", include("blog.api.urls"))
]
