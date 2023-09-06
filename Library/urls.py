"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BooksApp import views
from Users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/',views.home, name = "home_page"),
    path('books/',views.show_books, name = "all_active_books"),
    path('inactive-books/',views.show_inactive_books, name = "all_inactive_books"),
    path('update/<int:pk>/',views.update_book, name = "update_book"),
    path('delete/<int:pk>/',views.delete_book, name = "delete_book"),
    path('soft-delete/<int:pk>/',views.soft_delete_book, name = "soft_delete_book"),
    path('restore-book/<int:pk>/',views.restore_book, name = "restore_book"),
    path('create/', views.create_csv, name = "create_csv"),
    path('export/', views.export_xls, name = 'export_xls'),
    path('rawcsv/', views.raw_query_csv, name = 'raw_query_csv'),
    path('upload/', views.upload_csv, name = 'upload_csv'),




    # path('book-form/',views.book_form, name = "book_form"),
    # path('simple-form/',views.simple, name = "simple"),


# users url
#  
    # path('register/',user_views.register_request, name = "register"),
    # path('login/', user_views.login_request, name = "login_user"),
    # path('logout/', user_views.logout_user, name = "logout_user"),





]
