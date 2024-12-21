from django import forms

class loginForm(forms.Form):

    username = forms.CharField(label='Username', widget=forms.TextInput())

    password = forms.CharField(widget=forms.PasswordInput())
