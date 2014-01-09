import Image

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

def upload_to(instance, filename):
    return 'user_pics/'+str(instance.pk)+'/'+filename
DEFAULT_DIMENSIONS = (220, 265)

class User(AbstractUser):
    date_of_birth = models.DateField(_('date of birth'),
            blank=True, null=True)
    jabber = models.EmailField(_('jabber'), blank=True)
    skype = models.CharField(_('skype'), max_length=30, blank=True)
    photo = models.ImageField(_('photo'),
            upload_to = upload_to,
            blank=True,
            null=True,
            max_length=512)

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
                  'photo',
                  'jabber',
                  'skype',
                  'other_contacts',
                  'bio',
          ]



def resize_image(sender, **kwargs):
    user = kwargs["instance"]
    if user.photo:
        filename = user.photo.path
        img = Image.open(filename)
        img.thumbnail(DEFAULT_DIMENSIONS, Image.ANTIALIAS)
        img.save(filename)


post_save.connect(resize_image, sender=User)
