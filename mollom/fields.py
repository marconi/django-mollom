from django import forms

from mollom.widgets import ImageCaptchaInput

class MollomCaptchaField(forms.Field):
    """
    Custom mollom captcha field.
    """
    default_err_msg = u"Liar! You don't seem to be human at all."
    
    def __init__(self, error_msg=None, *args, **kwargs):
        self.error_msg = error_msg
        if not kwargs.get('widget', None):
            self.widget = ImageCaptchaInput()
        super(MollomCaptchaField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        super(MollomCaptchaField, self).clean(value)
        mollom_session = self.widget.captcha['session_id']
        if not self.widget.mollom.checkCaptcha(mollom_session, value):
            raise forms.ValidationError(self.error_msg or self.default_err_msg)
        return value