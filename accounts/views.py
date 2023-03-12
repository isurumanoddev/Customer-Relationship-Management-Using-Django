from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import *
from accounts.forms import *
from accounts.filters import OrderFilter, ProductFilter


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


def customers(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    print(orders)

    context = {"customer": customer, "orders": orders, "myFilter": myFilter}
    return render(request, "Customers.html", context)


def products(request):
    products = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {"products": products, "myFilter": myFilter}

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
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("home")
    context = {"form": form}
    return render(request, "register.html", context)


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


# def create_order(request, pk):
#     OrderFormSet = inlineformset_factory(Customer,Order,fields=("product","status"))
#     customer = Customer.objects.get(id=pk)
#     form_set = OrderFormSet(queryset=Order.objects.none(),instance=customer)
#     if request.method == "POST":
#         form_set = OrderFormSet(request.POST,instance=customer)
#         if form_set.is_valid():
#             form_set.save()
#             return redirect("/" )
#
#     context = {"form_set": form_set}
#     return render(request, "Order_form.html", context)
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


def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect("home")

    context = {"object": order}
    return render(request, "delete.html", context)


def create_customer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "Customer_form.html", context)


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


def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == "POST":
        customer.delete()
        return redirect("home")

    context = {"object": customer}
    return render(request, "delete.html", context)
