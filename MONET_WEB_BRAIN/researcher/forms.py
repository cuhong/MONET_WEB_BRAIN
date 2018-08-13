from django import forms
from django.urls import reverse

# django-crispy-forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions)

class SignupForm(forms.Form):
    name = forms.CharField(required=True, max_length=255, label='이름')
    email = forms.EmailField(required=True, label='이메일')
    pw = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput, label='비밀번호')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signup-form'
        self.helper.from_method = 'post'
        self.helper.form_action = reverse('researcher:sign_up')
        self.helper.add_input(Submit('submit', '시작', css_class='btn btn-primary btn-block', style='background-image: linear-gradient(-180deg, #34d058 0%, #28a745 90%); background-color: #28a745'))


class SigninForm(forms.Form):
    name = forms.CharField(required=True, max_length=255, label='이름')
    pw = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput, label='비밀번호')

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signin-form'
        self.helper.from_method = 'post'
        self.helper.form_action = reverse('researcher:sign_in')
        self.helper.add_input(Submit('submit', '시작', css_class='btn btn-primary btn-block', style='background-image: linear-gradient(-180deg, #34d058 0%, #28a745 90%); background-color: #28a745'))

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    comment = forms.CharField(widget=forms.Textarea)
    file = forms.FileField()
