from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.conf import settings

from PyMollom.Mollom import MollomBase

class CaptchaInput(Input):
    """
    Base captcha widget.
    """
    def __init__(self, attrs=None):
        self.mollom = MollomBase(settings.MOLLOM_CONFIG_FILE)
        super(CaptchaInput, self).__init__(attrs)

class ImageCaptchaInput(CaptchaInput):
    """
    Custom mollom image captcha widget.
    Displays an input field with the captcha image beside it.
    """
    def __init__(self, attrs=None):
        super(ImageCaptchaInput, self).__init__(attrs)
        self.captcha = self.mollom.getImageCaptcha()
        self.captcha_img = '<img src="%s" alt="captcha" />' % self.captcha['url']
    
    def render(self, name, value, attrs=None):
        self.captcha = self.mollom.getImageCaptcha(sessionID=self.captcha['session_id'])
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['value'] = '' # value should always be empty
        return mark_safe(u'<input%s /><span id="mcaptcha-image">%s</span>' % 
                        (flatatt(final_attrs), self.captcha_img))

class AudioCaptchaInput(CaptchaInput):
    """
    Custom mollom audio captcha widget.
    """
    def __init__(self, attrs=None):
        super(AudioCaptchaInput, self).__init__(attrs)
        self.captcha = self.mollom.getAudioCaptcha()

    def render(self, name, value, attrs=None):
        self.captcha = self.mollom.getAudioCaptcha(sessionID=self.captcha['session_id'])
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['value'] = '' # value should always be empty
        return mark_safe(u'<input%s /><span id="mcaptcha-audio">%s</span>' % 
                        (flatatt(final_attrs), self._build_player(self.captcha['url'])))
    
    def _build_player(self, url):
        out = '''<object width="300" height="42">
                <param name="src" value="%s">
                <param name="autoplay" value="false">
                <param name="controller" value="true">
                <param name="bgcolor" value="#FF9900">
                <embed src="%s" autostart="false" loop="false" width="300" height="42" controller="true"></embed>
                </object>''' % (url, url)
        return out