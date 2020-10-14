from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as lazy
from typing import Type


class UserManager(BaseUserManager):

    """
    Документация django рекомендует всегда создавать свою пользовательскую модель.

    А для своей модели - свой менеджер.
    """

    use_in_migrations = True

    def create_user(self, username: str, email: str, password: str, **kwargs) -> Type[BaseUserManager]:

        """
        Метод создания юзера.
        """

        if not email or not username:
            raise(lazy('Please, input all fields.'))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username: str, email: str, password: str, **kwargs) -> Type[BaseUserManager]:

        """
        Метод создания суперпользователя.

        Атрибутам присваиваются значения, а далее создание делегируется методу выше.
        """

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(lazy('superuser must have a is_staff=True'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(lazy('superuser must have a is_superuser=True'))

        return self.create_user(username, email, password, **kwargs)
