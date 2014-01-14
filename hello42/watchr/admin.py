from django.contrib import admin
from models import RecordedRequest, ModelChangeRecord

class RecorderRequestAdmin(admin.ModelAdmin):
    list_display = ('time',
                    'priority',
                    'path',
                    'method',
                    'user')
    class Meta:
        model = RecordedRequest

admin.site.register(RecordedRequest, RecorderRequestAdmin)
admin.site.register(ModelChangeRecord)
