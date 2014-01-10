from django.forms import Widget
from django.forms import DateInput
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput

class CustomClearableFileInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        url=value.url if value else ''
        display="block" if url else "none"
        checkbox_name = self.clear_checkbox_name(name)

        template = """
        <input id="{field_id}" type="file" value="" name="{name}">
        <img style="display:{display}" class="photopreview" src="{src}"><br>
        clear:
        <input id="{clear_checkbox_id}" type="checkbox" name="{clear_checkbox_name}">
        """.format(
            field_id='id_'+name, #TODO
            name=name,
            display=display,
            src=escape(url),
            clear_checkbox_id=self.clear_checkbox_id(checkbox_name),
            clear_checkbox_name=checkbox_name
        )

        return mark_safe(template)

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

