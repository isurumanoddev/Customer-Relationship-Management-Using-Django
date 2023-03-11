from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import *


# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    out_for_delevery = orders.filter(status="Out For Delivery").count()

    context = {"customers": customers, "orders": orders, "total_orders": total_orders, "delivered": delivered,
               "out_for_delevery": out_for_delevery, "pending": pending}
    return render(request, "Dashboard.html", context)


def customers(request,pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    context = {"customer": customer,"orders":orders}
    return render(request, "Customers.html", context)


def products(request):
    products = Product.objects.all()

    context = {"products": products}

    return render(request, "Products.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            print("User not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("<h1>Username or password incorrect</h1>")

    context = {}
    return render(request, "login.html", context)


def user_logout(request):
    logout(request)
    return redirect("home")


def user_register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("home")
    context = {"form": form}
    return render(request, "register.html", context)
