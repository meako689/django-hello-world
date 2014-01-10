from django.forms import Widget
from django.forms import DateInput


class CalendarDateInput(DateInput):
    """Js powered calendar"""
        
    class Media:
        css = {'all':('css/flick/jquery-ui-1.10.3.custom.css',)}
        js = ('js/jquery-1.9.1.js',
                'js/jquery-ui-1.10.3.custom.js',
                'js/CalendarDateInput.js')
            
    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'CalendarDateInput'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(CalendarDateInput, self).__init__(attrs=final_attrs, format=format)

