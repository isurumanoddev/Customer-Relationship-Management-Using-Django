from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import *
from accounts.decorators import *
from accounts.forms import *
from accounts.filters import OrderFilter, ProductFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.
@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    out_for_delevery = orders.filter(status="Out For Delivery").count()

    context = {"customers": customers, "orders": orders, "total_orders": total_orders, "delivered": delivered,
               "out_for_delivery": out_for_delevery, "pending": pending}
    return render(request, "Dashboard.html", context)


@login_required(login_url="login")
def customers(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    print(orders)

    context = {"customer": customer, "orders": orders, "myFilter": myFilter}
    return render(request, "Customers.html", context)


@login_required(login_url="login")
@allowed_user(["admin"])
def products(request):
    products = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {"products": products, "myFilter": myFilter}

    return render(request, "Products.html", context)


@unauthenticated_user
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
            messages.info(request, "Username or password incorrect")

    context = {}
    return render(request, "login.html", context)


def user_logout(request):
    logout(request)
    return redirect("home")


def user_register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            customer_group = Group.objects.get(name="customers")
            print(customer_group)
            user.groups.add(customer_group)

            login(request, user)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {username} ")
            return redirect("home")

    context = {"form": form}
    return render(request, "register.html", context)


@login_required(login_url="login")
@allowed_user(["admin"])
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={"customer": customer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer", pk=customer.id)

    context = {"form": form}
    return render(request, "Order_form.html", context)



@login_required(login_url="login")
@allowed_user(["admin"])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("customer", pk=order.customer.id)

    context = {"form": form}
    return render(request, "Order_form.html", context)


@login_required(login_url="login")
@allowed_user(["admin"])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect("home")

    context = {"object": order}
    return render(request, "delete.html", context)


@login_required(login_url="login")
@allowed_user(["admin"])
def create_customer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "Customer_form.html", context)


@login_required(login_url="login")
@allowed_user(["admin"])
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form, "customer": customer}
    return render(request, "Customer_form.html", context)


@login_required(login_url="login")
@allowed_user(["admin"])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("home")

    context = {"object": customer}
    return render(request, "delete.html", context)


def user_page(request):
    context = {}
    return render(request, "User.html", context)
