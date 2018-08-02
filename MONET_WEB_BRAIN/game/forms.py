from django import forms

class SigninForm(forms.Form):
    name = forms.CharField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'NAME'}), label='')
    pw = forms.CharField(required=True, min_length=3, max_length=50, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'PASSWORD'}), label='')

class SignupForm(forms.Form):
    name = forms.CharField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'NAME'}), label='')
    email = forms.EmailField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'E-mail'}), label='')
    pw = forms.CharField(required=True, min_length=3, max_length=50, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'PASSWORD'}), label='')