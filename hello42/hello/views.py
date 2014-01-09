from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy

from models import User, UserForm


def home(request):
    """Show info for users"""
    return render(request, 'hello/home.html',
                 {'users':User.objects.all()})

class UserEditView(UpdateView):
    """CBV time!"""
    template_name = 'hello/edit.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserEditView, self).dispatch(*args, **kwargs)

