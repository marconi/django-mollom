from django import forms
from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.conf import settings

from PyMollom.Mollom import MollomBase

class CaptchaInput(Input):
    """
    Custom mollom captcha widget.
    Displays an input field with the captcha image beside it.
    """
    def __init__(self, attrs=None):
        self.mollom = MollomBase(settings.MOLLOM_CONFIG_FILE)
        self.captcha = self.mollom.getImageCaptcha()
        self.captcha_img = '<img src="%s" alt="captcha" />' % self.captcha['url']
        super(CaptchaInput, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        self.captcha = self.mollom.getImageCaptcha(sessionID=self.captcha['session_id'])
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['value'] = '' # value should always be empty
        return mark_safe(u'<input%s /><span id="mcaptcha-image">%s</span>' % 
                        (flatatt(final_attrs), self.captcha_img))


class MollomCaptchaField(forms.Field):
    """
    Custom mollom captcha field.
    """
    default_err_msg = u"Liar! You don't seem to be human at all."
    
    def __init__(self, error_msg=None, *args, **kwargs):
        self.error_msg = error_msg
        self.widget = CaptchaInput()
        super(MollomCaptchaField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        super(MollomCaptchaField, self).clean(value)
        mollom_session = self.widget.captcha['session_id']
        if not self.widget.mollom.checkCaptcha(mollom_session, value):
            raise forms.ValidationError(self.error_msg or self.default_err_msg)
        return value