from django import forms

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import ReadOnlyPasswordHashField



User = get_user_model()


from django import forms

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import ReadOnlyPasswordHashField



User = get_user_model()



class UserAdminCreationForm(forms.ModelForm):

    """

    A form for creating new users. Includes all the required

    fields, plus a repeated password.

    """

    password = forms.CharField(widget=forms.PasswordInput)

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:

        model = User

        fields = ['email']

    # def clean(self):

    #     '''

    #     Verify both passwords match.

    #     '''

    #     cleaned_data = super().clean()

    #     password = cleaned_data.get("password")

    #     password2 = cleaned_data.get("password2")

    #     if password is not None and password != password2:

    #         self.add_error("password2", "Your passwords must match")

    #     return cleaned_data

    def clean_password2(self):

        # Check that the two password entries match

        password1 = self.cleaned_data.get("password")

        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:

            self.add_error("password2", "Your passwords must match")

        return password2

    def save(self, commit=True):

        # Save the provided password in hashed format

        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])

        if commit:

            user.save()

        return user

    


class UserAdminChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on

    the user, but replaces the password field with admin's

    password hash display field.

    """

    password = ReadOnlyPasswordHashField()

    class Meta:

        model = User

        fields = ['email', 'password', 'is_active', 'is_superuser']

    def clean_password(self):

        # Regardless of what the user provides, return the initial value.

        # This is done here, rather than on the field, because the

        # field does not have access to the initial value

        return self.initial["password"]
