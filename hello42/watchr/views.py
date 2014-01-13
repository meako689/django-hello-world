from django.shortcuts import render
from models import RecordedRequest

# Create your views here.

def request_list(request):
    """show latest requests to site"""
    order_by = request.GET.get('order_by')
    qs = RecordedRequest.objects.all()
    if order_by:
        allowed_fields =[f.name for f in RecordedRequest._meta.fields]
        if order_by.replace('-','') in allowed_fields:
            qs = RecordedRequest.objects.order_by(order_by)
    return render(request, 'watchr/list.html',
            {'request_list':qs[:10]})
