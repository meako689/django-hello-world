from django.db import models
from hello.models import User
from json_field import JSONField

# Create your models here.

class RecordedRequest(models.Model):
    """Database stored representation of HttpRequest object"""
    time = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    path = models.CharField(max_length=1024)
    path_info = models.CharField(max_length=1024)
    method = models.CharField(max_length=4)
    encoding = models.CharField(max_length=16,
                null=True,blank=True)
    get = JSONField()
    post = JSONField()
    cookies = JSONField()
    user = models.ForeignKey(User,blank=True, null=True)

    @classmethod
    def from_request(cls, request):
        user = request.user if request.user.is_authenticated() else None
        obj = cls.objects.create(body=request.body,
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

