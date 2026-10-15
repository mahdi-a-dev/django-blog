from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "status", "category", "created_date", "published_date")
    list_filter = ("author", "status", "category")

    ordering = ("-published_date",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "profile", "created_date", "updated_date")
    search_fields = ('content', 'profile__user__email', "post__title")