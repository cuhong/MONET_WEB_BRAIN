from django import forms
from django.urls import reverse

# django-crispy-forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions)
from crispy_forms.layout import Submit, Layout, Div, Fieldset
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab

# django auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    parent_email = forms.EmailField(required=False, label='부모님 이메일')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signup-form'
        self.helper.from_method = 'post'
        self.helper.form_action = reverse('game:sign_up')
        self.helper.add_input(Submit('submit', '시작', css_class='btn btn-primary btn-block', style='background-image: linear-gradient(-180deg, #34d058 0%, #28a745 90%); background-color: #28a745'))
        self.helper.layout = Layout(
            Fieldset('필수 입력 사항', 'username', 'email', 'password1', 'password2'),
            Fieldset('미성년자 추가 입력사항', 'parent_email')
        )

    class Meta:
        model = User
        fields= ('username', 'email', 'password1', 'password2')

"""
class SignupForm(forms.Form):
    name = forms.CharField(required=True, max_length=255, label='이름')
    email = forms.EmailField(required=True, label='이메일')
    pw = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput, label='비밀번호')
    is_adult = forms.BooleanField(required=False, label='미성년자 이신가요?')
    parent_email = forms.EmailField(required=False, label='부모님 이메일')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signup-form'
        self.helper.from_method = 'post'
        self.helper.form_action = reverse('game:sign_up')
        self.helper.add_input(Submit('submit', '시작', css_class='btn btn-primary btn-block', style='background-image: linear-gradient(-180deg, #34d058 0%, #28a745 90%); background-color: #28a745'))
        self.helper.layout = Layout(
            Fieldset('필수 입력 사항', 'name', 'email', 'pw'),
            Fieldset('미성년자 추가 입력사항', 'parent_email')
        )
"""

class SigninForm(forms.Form):
    name = forms.CharField(required=True, max_length=255, label='이름')
    pw = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput, label='비밀번호')

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signin-form'
        self.helper.from_method = 'post'
        self.helper.form_action = reverse('game:sign_in')
        self.helper.add_input(Submit('submit', '시작', css_class='btn btn-primary btn-block', style='background-image: linear-gradient(-180deg, #34d058 0%, #28a745 90%); background-color: #28a745'))


class AuthForm(forms.Form):
    auth_code = forms.CharField(required=True, max_length=255, label='암호')

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-auth-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', '시작', css_class='btn btn-primary btn-block', style='background-image: linear-gradient(-180deg, #34d058 0%, #28a745 90%); background-color: #28a745'))
