from django.db import models


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
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    author = models.CharField(max_length=120, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    # за умовою image — це посилання (а не завантаження файлу)
    image = models.URLField(blank=True, verbose_name="URL зображення")
    publication_date = models.DateField(verbose_name="Дата публікації")
    is_published = models.BooleanField(default=False, verbose_name="Опубліковано")

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,    # не даємо видалити кат., якщо є статті
        related_name="articles",
        verbose_name="Категорія",
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="articles",
        blank=True,
        verbose_name="Теги",
    )

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"
        ordering = ("-publication_date", "title")
        indexes = [
            models.Index(fields=["is_published", "publication_date"]),
        ]

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст")
    author = models.CharField(max_length=120, verbose_name="Автор")
    publication_date = models.DateField(verbose_name="Дата публікації")
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,    # видаляємо коментарі разом зі статтею
        related_name="comments",
        verbose_name="Стаття",
    )

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ("-publication_date",)

    def __str__(self) -> str:
        return f"{self.author}: {self.text[:30]}..."
