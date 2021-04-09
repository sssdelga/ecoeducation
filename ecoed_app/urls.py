from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    # user pages
    path('registration', views.reg_user),
    path('create_user', views.create_user),
    path('login', views.login_user),
    path('subscribe', views.subscribe),
    path('hello/<str:user_fname>', views.user_home),
    path('logout', views.logout),
    path('carbon/log', views.log_carbon),

    path('books/<int:book_id>', views.view_book)
]