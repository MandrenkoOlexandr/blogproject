from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from myblog.models import Comment

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Після будь-якої міграції гарантуємо наявність груп:
      - Автор: може додавати коментарі, а ще має кастомні права на зміну/видалення тільки своїх.
      - Модератор: все, що автор, + повні права на зміну/видалення будь-яких.
    """
    # content type для моделі Comment
    ct = ContentType.objects.get_for_model(Comment)

    # стандартні права
    add_comment = Permission.objects.get(codename="add_comment", content_type=ct)
    change_comment = Permission.objects.get(codename="change_comment", content_type=ct)
    delete_comment = Permission.objects.get(codename="delete_comment", content_type=ct)
    view_comment = Permission.objects.get(codename="view_comment", content_type=ct)

    # кастомні права
    change_own = Permission.objects.get(codename="change_own_comment", content_type=ct)
    delete_own = Permission.objects.get(codename="delete_own_comment", content_type=ct)
    delete_any = Permission.objects.get(codename="delete_any_comment", content_type=ct)

    # Група Автор
    author_group, _ = Group.objects.get_or_create(name="Автор")
    author_group.permissions.set({view_comment, add_comment, change_own, delete_own})
    author_group.save()

    # Група Модератор
    moderator_group, _ = Group.objects.get_or_create(name="Модератор")
    moderator_group.permissions.set({
        view_comment, add_comment, change_comment, delete_comment, delete_any,
        change_own, delete_own  # включає і “власні” дії
    })
    moderator_group.save()
