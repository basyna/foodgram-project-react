from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Login пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Почта пользователя',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        blank=False,
    )
    password = models.CharField(
        'Пароль для пользователя',
        max_length=150,
        blank=False,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='name of constraint'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
