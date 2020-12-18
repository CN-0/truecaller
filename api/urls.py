from django.contrib import admin
from django.urls import path, include
from .views import SignupView, LoginView, SpamView, SearchView, ContactsView

urlpatterns = [
    path('', ContactsView.as_view()),
    path('register/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('spam/', SpamView.as_view()),
    path('search/', SearchView.as_view())
]
