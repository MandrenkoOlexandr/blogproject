from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    # зберігаємо рядок класу Font Awesome, напр. "fa-solid fa-book"
    icon = models.CharField(max_length=100, blank=True, verbose_name="Іконка (FontAwesome)")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name="Тег")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)   # імʼя авторa (анонім)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )
    text = models.TextField()
    image = models.CharField(max_length=255, blank=True)
    publication_date = models.DateField()
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True)  # анонімне імʼя
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments"
    )
    publication_date = models.DateField()
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ("-publication_date",)

        permissions = [
            ("change_own_comment", "Can change own comment"),
            ("delete_own_comment", "Can delete own comment"),
            ("delete_any_comment", "Can delete any comment"),
        ]

    def __str__(self):
        return self.text[:30]
