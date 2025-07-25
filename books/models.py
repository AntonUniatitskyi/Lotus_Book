from django.db import models
from django.contrib.auth.models import User
from core import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests
import os
from core.settings import GOOGLE_BOOKS
from unidecode import unidecode
# Create your models here.

class Profile(models.Model):
    AVATAR_CHOICES = [
        ('avatars/default-avatar.jpg', 'Дефолт'),
        ('avatars/boy-brunet.png', 'Брюнет'),
        ('avatars/girl-blond-long.png', 'Блондинка'),
        ('avatars/girl-brunet-long.png', 'Брюнетка'),
        ('avatars/girl-brunet-short.png', 'Коротка брюнетка'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default-avatar.jpg')
    avatar = models.CharField(max_length=255, choices=AVATAR_CHOICES, blank=True, default='avatars/default-avatar.jpg')

    def __str__(self): return f"Профиль пользователя {self.user.username}"

    def get_avatar_url(self):
        if self.avatar:
            return f"{settings.MEDIA_URL}{self.avatar}"
        return f"{settings.MEDIA_URL}avatars/default-avatar.jpg"

class Book(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='books')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    text_author = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author} ({self.created_at.strftime('%Y-%m-%d')})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.slug:
            self.slug = slugify(unidecode(f"{self.title}-{self.author}"))

        if is_new and not self.cover:
            try:
                filename = slugify(unidecode(f"{self.title} {self.author}")) + ".jpg"
                local_path = os.path.join(settings.MEDIA_ROOT, "covers", filename)

                if os.path.exists(local_path):
                    # Файл уже существует — просто подключаем
                    self.cover.name = f"covers/{filename}"
                else:
                    # Иначе скачиваем
                    query = f"{self.title} {self.author}"
                    url = "https://www.googleapis.com/books/v1/volumes"
                    params = {
                        'q': query,
                        'key': GOOGLE_BOOKS,
                        'maxResults': 1,
                        'printType': 'books',
                        'langRestrict': 'ru'
                    }
                    response = requests.get(url, params=params)
                    data = response.json()

                    items = data.get("items")
                    if items:
                        volume_info = items[0].get("volumeInfo", {})
                        image_links = volume_info.get("imageLinks", {})
                        thumbnail_url = image_links.get("thumbnail")

                        if thumbnail_url:
                            thumbnail_url = thumbnail_url.replace("http://", "https://")
                            image_response = requests.get(thumbnail_url)
                            if image_response.status_code == 200:
                                self.cover.save(filename, ContentFile(image_response.content), save=False)
            except Exception as e:
                print(f"Ошибка при получении обложки из Google Books: {e}")

        super().save(*args, **kwargs)

class BookQuote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes_user')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Цитата от {self.created_at.strftime('%d.%m.%Y')}"