from django.contrib import admin
from .models import Category, Tag, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "icon")
    search_fields = ("title",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("author", "text", "publication_date")
    readonly_fields = ()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "publication_date", "is_published")
    list_filter = ("is_published", "category", "tag")
    search_fields = ("title", "author", "text")
    date_hierarchy = "publication_date"
    filter_horizontal = ("tag",)
    inlines = (CommentInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "article", "publication_date")
    list_filter = ("publication_date", "article")
    search_fields = ("author", "text")
