import json
from django.http import HttpResponse
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

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            if self.object.photo:
                photo = self.object.photo.url
            else:
                photo = ''
            data = {
                'pk': self.object.pk,
                'photo': photo
            }
            return self.render_to_json_response(data)
        else:
            return response

class UserEditView(AjaxableResponseMixin, UpdateView):
    """CBV time!"""
    template_name = 'hello/edit.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserEditView, self).dispatch(*args, **kwargs)

