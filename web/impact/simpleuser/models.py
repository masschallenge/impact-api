# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

"""
Code from this app is taken from JamBon SW's internal best-practices
user model.  JamBon SW is planning to open source this code before March
under a BSD 2-clause license. This will allow for this entire app to be
removed by MC, if so desired.
"""
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves an User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('An email address must be provided.')
        email = self.normalize_email(email)
        if "is_active" not in extra_fields:
            extra_fields["is_active"] = True
        user = self.model(email=email,
                          is_staff=is_staff, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class SimpleIdentityMixin(models.Model):
    """
    A mixin class that provides a simple first name/last name
    representation of user identity.
    """
    full_name = models.CharField(
        _('full name'),
        max_length=200,
        blank=True,
        db_column='first_name')
    short_name = models.CharField(
        _('short name'),
        max_length=50,
        db_column='last_name')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into the admin site.'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        abstract = True


class AbstractUser(SimpleIdentityMixin, PermissionsMixin, AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions, using email as a username.

    All fields other than email and password are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'short_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class User(AbstractUser):
    """
    The abstract base class exists so that it can be easily extended,
    but this class is the one that should be instantiated.
    """
    username = models.CharField(_('username'), max_length=150, blank=True)

    class Meta:
        managed = False
        db_table = 'auth_user'

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)
