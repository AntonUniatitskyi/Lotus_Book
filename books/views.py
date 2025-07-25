from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from . import forms
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.contrib import messages
from .forms import UserForm, UserEditForm, ProfileForm, BookQuoteForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, View, UpdateView
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, BookQuote
from core import settings
from django.urls import reverse


# Create your views here.
def home(request):
    recent_quotes = BookQuote.objects.select_related('book').order_by('-id')[:4]
    return render(request, 'books/home.html', {'recent_quotes': recent_quotes})

# @login_required
# def all_quotes(request):
#     quotes = BookQuote.objects.select_related('book').order_by('-created_at')
#     return render(request, 'books/all_quotes.html', {'quotes': quotes})

class All_QuotesView(LoginRequiredMixin, ListView):
    model = BookQuote
    template_name = 'books/all_quotes.html'
    context_object_name = 'quotes'

def add_user(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                request.session['username'] = user.username
                # if user.email in core.settings.ADMIN_EMAIL:
                #     group = Group.objects.get(name="Адміністратор")
                #     user.groups.add(group)
                # else:
                #     group = Group.objects.get(name="Користувач")
                #     user.groups.add(group)

                login(request, user)  # автоматический вход
                next_url = request.POST.get('next', '/')
                return redirect(next_url)
            except IntegrityError:
                messages.error(request, 'Користувач з такою поштою вже зареєстрований.')
        else:
            print(form.errors)
            messages.error(request, 'Виникла помилка. Перевірте введені дані.')
    else:
        form = UserForm()
    return render(request, 'books/register.html', {'form': form, 'next': request.GET.get('next', '/')})

class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        return render(request, 'books/settings.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'MEDIA_URL': settings.MEDIA_URL
        })

    def post(self, request):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            # Если аватар НЕ выбран — сохранить старый
            avatar = profile_form.cleaned_data.get('avatar')
            if avatar:
                request.user.profile.avatar = avatar
            # иначе — avatar останется прежним

            request.user.profile.bio = profile_form.cleaned_data.get('bio')
            request.user.profile.save()

            login(request, request.user)
            return redirect('account')

        return render(request, 'books/settings.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'MEDIA_URL': settings.MEDIA_URL
        })

class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = forms.BookForm
    template_name = 'books/add_book.html'

    def form_valid(self, form):
        if hasattr(self.request.user, 'profile'):
            form.instance.profile = self.request.user.profile
        else:
            # Обработка случая, если профиль отсутствует
            raise ValueError("User has no profile")
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('account')

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book_det'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote_form'] = BookQuoteForm()
        return context


class AddQuoteView(LoginRequiredMixin, CreateView):
    model = BookQuote
    form_class = BookQuoteForm

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['book_id'], profile=self.request.user.profile)
        form.instance.book = book
        form.instance.user = self.request.user
        response = super().form_valid(form)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            quote = self.object
            return JsonResponse({
                "text": quote.text,
                "created_at": localtime(quote.created_at).strftime("%d.%m.%Y %H:%M")
            })

        return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"errors": form.errors}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('book_detail', kwargs={'slug': self.object.book.slug})

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'books/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        books = user.profile.books.all()

        context['books'] = books
        return context