from django import forms


from django.contrib.auth import (
    get_user_model, password_validation
)
User = get_user_model()


class loginForm(forms.Form):

    username = forms.CharField(label='Username', widget=forms.TextInput())

    password = forms.CharField(widget=forms.PasswordInput())


class registerForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
    ), strip=False, help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(
    ), strip=False, help_text="Both Passwords should be same.",)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
        ]

    def clean_password2(self):
        cd = self.cleaned_data
        if self.cleaned_data.get('password') != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)