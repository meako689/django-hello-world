from django.shortcuts import render
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

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['half'] = len(context['form'].fields)/2
        return context
