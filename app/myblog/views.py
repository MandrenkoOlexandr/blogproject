from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.utils import timezone

from .models import Article, Category, Tag, Comment


def home(request):
    articles = (
        Article.objects.filter(is_published=True, publication_date__lte=timezone.now().date())
        .select_related("category")
        .prefetch_related("tag")
        .order_by("-publication_date")[:3]
    )
    return render(request, "myblog/home.html", {"articles": articles})


def article_list(request):
    qs = (
        Article.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("tag")
        .order_by("-publication_date")
    )
    category_id = request.GET.get("category")
    tag_id = request.GET.get("tag")
    if category_id:
        qs = qs.filter(category_id=category_id)
    if tag_id:
        qs = qs.filter(tag__id=tag_id)

    context = {
        "articles": qs,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "active_category": int(category_id) if category_id else None,
        "active_tag": int(tag_id) if tag_id else None,
    }
    return render(request, "myblog/article_list.html", context)


def article_detail(request, pk: int):
    article = get_object_or_404(
        Article.objects.select_related("category").prefetch_related("tag", "comments"),
        pk=pk,
        is_published=True,
    )
    return render(request, "myblog/article_detail.html", {"article": article})


def add_comment(request, pk: int):
    # простий POST без форми (для навчальної задачі)
    if request.method != "POST":
        return redirect("myblog:article_detail", pk=pk)

    article = get_object_or_404(Article, pk=pk, is_published=True)
    text = request.POST.get("text", "").strip()
    author = request.POST.get("author", "").strip()
    if text and author:
        Comment.objects.create(text=text, author=author, publication_date=timezone.now().date(), article=article)
    return redirect("myblog:article_detail", pk=pk)
