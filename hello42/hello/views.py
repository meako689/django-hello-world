from django.shortcuts import render
from models import User
# Create your views here.
def home(request):
    """Show info for users"""
    return render(request, 'hello/home.html',
                 {'users':User.objects.all()})
