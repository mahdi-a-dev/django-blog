from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    # get list of post objects, Its supports GET and POST methods
    path("post/", views.post_list, name="api-post-list"),
    # get single post object, Its supports GET, PUT, DELETE methods
    path("post/<int:pk>", views.post_detail, name="api-post-detail"),
]