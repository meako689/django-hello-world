from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    jabber = models.EmailField(_('jabber'), blank=True)
    skype = models.CharField(_('skype'), max_length=30, blank=True)
    bio = models.TextField(_('bio'), blank=True)
    other_contacts = models.TextField(_('other'), blank=True)

    class Meta:
        abstract = False

class UserForm(forms.ModelForm):
    """edit user"""
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'date_of_birth',
                  'email',
                  'jabber',
                  'skype',
                  'other_contacts',
                  'bio',
          ]


