from django import forms

class SigninForm(forms.Form):
    name = forms.CharField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'NAME'}), label='')
    pw = forms.CharField(required=True, min_length=3, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'PASSWORD'}), label='')

class SignupForm(forms.Form):
    name = forms.CharField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'NAME'}), label='')
    email = forms.EmailField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'E-mail'}), label='')
    pw = forms.CharField(required=True, min_length=3, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'PASSWORD'}), label='')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    comment = forms.CharField(widget=forms.Textarea)
    file = forms.FileField()
