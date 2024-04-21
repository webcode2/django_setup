from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import EmailField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime
# from typing import

from account.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email: EmailField = models.EmailField(unique=True, max_length=255, blank=False, )

    # All these field declarations are copied as-is    # from `AbstractUser`
    first_name: str = models.CharField(_('first name'), max_length=30, blank=False)
    last_name: str = models.CharField(_('last name'), max_length=150, blank=False )
    is_staff: bool = models.BooleanField(_('staff status'), default=False,
                                         help_text=_('Designates whether the user can log into '
                                                     'this admin site.'
                                                     ),
                                         )
    is_active: bool = models.BooleanField(_('active'),
                                          default=True,
                                          help_text=_('treated as active. Unselect this instead '
                                                      'of deleting accounts.'))

    date_joined: datetime = models.DateTimeField(_('date joined'), default=timezone.now, )

    def __str__(self):
        return self.email

    def get_full_name(self) -> str:
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """
        Returns the short name for the user.
        """
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # Add additional fields here if needed

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
