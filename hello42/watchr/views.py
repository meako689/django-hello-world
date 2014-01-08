from django.shortcuts import render
from models import RecordedRequest

# Create your views here.

def request_list(request):
    """show latest requests to site"""
    return render(request, 'watchr/list.html',
            {'request_list':RecordedRequest.objects.all()[:10]})
