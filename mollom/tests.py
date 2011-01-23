from django.test import TestCase

from mollom.forms import MockSignupForm

class MollomTest(TestCase):
    
    def testCaptchaField(self):
        form = MockSignupForm()
        self.failUnless(form.fields['captcha'])
    
    def testEmptyCaptchaField(self):
        test_data = {
            'data': {'username': 'marc',
                     'email': 'marc@example.com',
                     'password1': 'supersecure',
                     'password2': 'supersecure',
                     'captcha': ''},
            'error': ('captcha', [u"This field is required."])
        }
        signup_form = MockSignupForm(data=test_data['data'])
        self.failIf(signup_form.is_valid())
        self.assertEqual(signup_form.errors[test_data['error'][0]],
                         test_data['error'][1])
    
    def testInvalidCaptcha(self):
        test_data = {
            'data': {'username': 'marc',
                     'email': 'marc@example.com',
                     'password1': 'supersecure',
                     'password2': 'supersecure',
                     'captcha': 'randomstuff4321'},
            'error': ('captcha', [u"Liar! You don't seem to be human at all."])
        }
        signup_form = MockSignupForm(data=test_data['data'])
        self.failIf(signup_form.is_valid())
        self.assertEqual(signup_form.errors[test_data['error'][0]],
                         test_data['error'][1])
