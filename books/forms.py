from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.forms import EmailInput, CharField, PasswordInput, TextInput, RadioSelect
from django import forms
from .models import Profile, Book, BookQuote

class UserPasswordForm(AuthenticationForm):
    username = CharField(
        widget=TextInput(attrs={
            'class': 'form-control',
        })
    )
    password = CharField(
        widget=PasswordInput(attrs={
            'id': 'id_password',
            'data-target': 'id_password',
            'class': 'form-control',
        })
    )

    class Meta:
        fields = ['username', 'password']

class UserForm(UserCreationForm):
    password1 = CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'id': 'id_password1',
            'data-toggle': 'password',
        })
    )
    password2 = CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'id': 'id_password2',
            'data-toggle': 'password',
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
            }),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']
        widgets = {
            'email': EmailInput(),
            'username': TextInput()
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'text_author']
        widgets = {
            'title': TextInput(attrs={
                'id': 'id_title',
                'class': 'form-control',
                'placeholder': 'Название книги'
            }),
            'author': TextInput(attrs={
                'id': 'id_author',
                'class': 'form-control',
                'placeholder': 'Автор книги'
            }),
            'text_author': forms.Textarea(attrs={
                'id': 'id_text_author',
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Факт о авторе...'
            })
        }

class ProfileForm(forms.ModelForm):
    avatar = forms.ChoiceField(
        choices=Profile.AVATAR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'avatar-radio hidden'}),
        required=False  # <-- важно!
    )

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'id': 'id_bio',
                'rows': 4,
                'placeholder': 'Немного про себя...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Установим текущее значение в форме, чтобы "выбрало" текущее
        if self.instance and self.instance.avatar:
            self.initial['avatar'] = self.instance.avatar


class BookQuoteForm(forms.ModelForm):
    class Meta:
        model = BookQuote
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control w-full p-3 rounded border border-gray-300 focus:outline-none focus:ring focus:border-blue-400',
                'rows': 3,
                'placeholder': 'Введите цитату...'
            })
        }
