from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customers, name="customer"),

    path('user/', views.user_page, name="user-page"),
    path('account/<str:pk>', views.account_settings, name="settings-page"),

    path('create_order/<str:pk>', views.create_order, name="create-order"),
    path('update_order/<str:pk>', views.update_order, name="update-order"),
    path('delete_order/<str:pk>', views.delete_order, name="delete-order"),

    path('create_customer/', views.create_customer, name="create-customer"),
    path('update_customer/<str:pk>', views.update_customer, name="update-customer"),
    path('delete_customer/<str:pk>', views.delete_order, name="delete-customer"),

    path('user_login/', views.user_login, name="login"),
    path('user_logout/', views.user_logout, name="logout"),
    path('user_register/', views.user_register, name="register"),

]
