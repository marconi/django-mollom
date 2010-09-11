from django import forms
from django.conf import settings
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import force_unicode

from django_mollom.pymollom.Mollom import MollomBase

class CaptchaInput(Widget):
    
    input_type = 'text'
    
    def __init__(self, img_url, attrs=None):
        self.captcha_img = '<img src="%s" />' % img_url
        super(CaptchaInput, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'<input%s />%s' % (flatatt(final_attrs),
                                               self.captcha_img))

class MollomCaptchaField(forms.CharField):
    
    default_err_msg = u"Liar! You don't seem to be human at all."
    
    def __init__(self, error_message=None, *args, **kwargs):
        self.mollom = MollomBase(settings.MOLLOM_CONFIG_FILE)
        self.captcha = self.mollom.getImageCaptcha()
        self.widget = CaptchaInput(img_url=self.captcha['url'])
        self.err_msg = error_message
        super(MollomCaptchaField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        super(MollomCaptchaField, self).clean(value)
        mollom_session = self.captcha['session_id']
        if not self.mollom.checkCaptcha(mollom_session, value):
            self.captcha = self.mollom.getImageCaptcha(sessionID=mollom_session)
            raise forms.ValidationError(self.err_msg or self.default_err_msg)
        captcha = self.mollom.getImageCaptcha()        
        return value