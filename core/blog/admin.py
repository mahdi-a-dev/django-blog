from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "status", "category", "created_date", "published_date")
    list_filter = ("author", "status", "category")
    search_fields = ("title", "author", "category")
    raw_id_fields = ("author", "category")
    date_hierarchy = "published_date"
    ordering = ("-status", "-published_date",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "profile", "parent", "created_date", "updated_date")
    search_fields = ('content', 'profile__user__email', "post__title")
    raw_id_fields = ("post", "profile", "parent")
    date_hierarchy = "created_date"
    ordering = ("-created_date",)