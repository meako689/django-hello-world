from django.db import models
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save, pre_delete
from hello.models import User
from json_field import JSONField
from django.conf import settings

# Create your models here.

class RecordedRequest(models.Model):
    """Database stored representation of HttpRequest object"""
    priority = models.SmallIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True,blank=True)
    path = models.CharField(max_length=1024)
    path_info = models.CharField(max_length=1024)
    method = models.CharField(max_length=4)
    encoding = models.CharField(max_length=16,
                null=True,blank=True)
    get = JSONField(null=True,blank=True)
    post = JSONField(null=True,blank=True)
    cookies = JSONField(null=True,blank=True)
    user = models.ForeignKey(User,blank=True, null=True)

    @classmethod
    def from_request(cls, request):
        user = request.user if request.user.is_authenticated() else None
        obj = cls.objects.create(body=request.body.encode('base64'),
                path=request.path,
                path_info=request.path_info,
                method=request.method,
                encoding=request.encoding,
                get=request.GET,
                post=request.POST,
                cookies=request.COOKIES,
                user=user)
        return obj

    def __unicode__(self):
        return 'Request: {path}, method:{method}'.format(path=self.path,
                method=self.method)

ACTION_CHOICES = (
        (1,'Create'),
        (2,'Update'),
        (3,'Delete'),
    )

class ModelChangeRecord(models.Model):
    """When model get changed, we create new entry"""
    time = models.DateTimeField(auto_now_add=True)
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    shelfed_object = JSONField()

    def __unicode__(self):
        return "Rec for {obj}, action: {act}, at {date}".format(
                obj=self.content_object,
                act=self.get_action_display(),
                date=self.time
    )

    @classmethod
    def create_rec(cls, action, obj):
        return ModelChangeRecord.objects.create(action=action,
                content_object=obj,
                shelfed_object=serializers.serialize('json',(obj,))
        )

def record_create_update(sender, **kwargs):
    if not kwargs['raw']:
        if kwargs['created']:
            action = 1
        else:
            action = 2
        obj = kwargs['instance']
        ModelChangeRecord.create_rec(action, obj)

def record_delete(sender, **kwargs):
    ModelChangeRecord.create_rec(action=3, obj=kwargs['instance'])

#attach to everything
for model in models.get_models():

    if model.__name__ not in settings.EXCEPT_MODELS:
        post_save.connect(record_create_update,
                sender=model, dispatch_uid="watch-"+model.__name__)
        pre_delete.connect(record_delete,
                sender=model, dispatch_uid="watch-"+model.__name__)
