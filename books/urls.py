from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import forms
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='books/login.html',
                                                authentication_form=forms.UserPasswordForm),
                                                name='login'),
    path('register/', views.add_user, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/', views.UpdateProfileView.as_view(), name='settings'),
    path('add_book', views.AddBookView.as_view(), name='add_book'),
    path('account', views.ProfileView.as_view(), name='account'),
    path('book/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add_quote/<int:book_id>', views.AddQuoteView.as_view(), name='add_quote'),
    path("all_quotes", views.All_QuotesView.as_view(), name="all_quotes"),
]