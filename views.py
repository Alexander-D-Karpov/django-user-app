from django.contrib import auth
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from main.models import Post
from .forms import CustomUserChangeForm
from .forms import CustomUserCreationForm
from .models import Person, TgAccount


def login(request):
    url = request.META.get('HTTP_REFERER')
    if not url:
        url = ""
    if request.method == "POST":
        req_from = request.GET["from"]
        username, password = request.POST["username"], request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if req_from:
                return redirect(req_from)
            return redirect("index")

        else:
            messages.error(request, "Wrong username or password")

    return render(request, "user/login.html", context={"url": url})


def logout(request):
    auth.logout(request)
    return render(request, "user/logout.html")


def register(request):
    url = request.META.get('HTTP_REFERER')
    if not url:
        url = ""
    if request.method == "POST":
        req_from = request.GET["from"]
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            n = f.save()
            auth.login(request, n)
            if req_from:
                return redirect(req_from)

        else:
            messages.error(request, "Some of the fields dont match requirements")

    else:
        f = CustomUserCreationForm()

    return render(request, "user/register.html", {"form": f, "url": url})


def settings(request):
    tg_secret = None
    f = None
    if request.user.is_authenticated:
        if request.method == "POST":
            f = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
            if f.is_valid():
                f.save()
                return redirect("index")
            else:
                return render(request, "user/settings.html", {"form": f})
        else:
            tg_secret = TgAccount.objects.get_or_create(user=request.user)[0]
            f = CustomUserChangeForm()
    return render(request, "user/settings.html", {"form": f, "tg_secret": tg_secret})


def tg_unlink(request):
    if request.method == "POST":
        if TgAccount.objects.filter(user=request.user).exists():
            user = TgAccount.objects.get(user=request.user)
            user.username = None
            user.varified = False
            user.save()
    return redirect("settings")


def user_list(request):
    users = Person.objects.all()
    return render(request, "user/user_list.html", {"users": users})


def profile(request, username):
    user = get_object_or_404(Person, username=username)
    posts = Post.objects.filter(creator__username=username)
    if tg_user := TgAccount.objects.filter(user=user):
        tg_user = tg_user[0].username
    return render(
        request, "user/profile.html", {"u": user, "tg_user": tg_user, "posts": posts}
    )
