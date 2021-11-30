from django.db import models
from django.contrib.auth.models import AbstractUser

from .config import ADMIN, MODER, USER


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
        max_length=254,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
    )
    first_name = models.CharField(
        null=True,
        max_length=35,
        blank=True,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        null=True,
        max_length=35,
        blank=True,
        verbose_name='Фамилия пользователя',
    )
    password = models.CharField(
        null=True,
        max_length=90,
        blank=True,
        verbose_name='Пароль пользователя',
    )

    class Role(models.TextChoices):
        USER = USER, USER
        MODERATOR = MODER, MODER
        ADMIN = ADMIN, ADMIN

    role = models.CharField(
        max_length=9,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Уровень аккаунта',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('role', 'username', 'password')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    def is_user(self):
        return self.role == self.Role.USER


class Follow(models.Model):
    """Описывает работу подписок."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'

    class Meta:
        db_table = 'Follow'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', ],
                name='user_unique',
            )
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_following'
            )
        ]
