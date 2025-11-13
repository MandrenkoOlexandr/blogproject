from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # додати в групу Автор
            author_group = Group.objects.get(name="Автор")
            author_group.user_set.add(user)

            # автоматично логінити після реєстрації
            login(request, user)

            return redirect("myblog:home")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
