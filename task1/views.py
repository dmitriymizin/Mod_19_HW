from django.shortcuts import render
from .forms import UserRegister
from .models import Buyer, Game

# Create your views here.
def menu_view(request):
    return render(request, 'menu.html')

def games_view(request):
    games = Game.objects.all()
    return render(request, 'games.html', {'games': games})

def platform_view(request):
    return render(request, 'platform.html')

def cart_view(request):
    cart_items = []
    return render(request, 'cart.html', {'cart_items': cart_items})

users = ["user1", "user2"]

def sign_up_by_html(request):
    info = {}
    if request.method == 'POST':
        username = request.POST.get("login")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        age = request.POST.get("age")

        if password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif int(age) < 18:
            info['error'] = 'Вы должны быть старше 18'
        elif Buyer.objects.filter(name=username).exists():
            info['error'] = 'Пользователь уже существует'
        else:
            Buyer.objects.create(name=username, age=age, balance=0)
            info['error'] = f'Приветствуем, {username}!'

    return render(request, "registration_page.html", info)

def sign_up_by_django(request):
    info = {}
    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            repeat_password = form.cleaned_data["repeat_password"]
            age = form.cleaned_data["age"]

            if password != repeat_password:
                info["error"] = "Пароли не совпадают"
            elif int(age) < 18:
                info["error"] = "Вы должны быть старше 18"
            elif Buyer.objects.filter(name=username).exists():
                info["error"] = "Пользователь уже существует"
            else:
                Buyer.objects.create(name=username, age=age, balance=0)
                info["error"] = f"Приветствуем, {username}!"
        else:
            info["form"] = form
    else:
        info["form"] = UserRegister()

    return render(request, "registration_page.html", info)