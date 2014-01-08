from django.conf import settings

def settings_context(request):
    """docstring for settings_context"""
    return {'settings':settings}
