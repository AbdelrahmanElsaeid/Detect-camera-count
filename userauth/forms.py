


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,BillingInfo

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    organization = forms.CharField(required=True)
    
    class Meta:
        model = User
        #fields = ("email", "username", "organization", "password")
        fields = ("email", "username", "organization", "password1", "password2")


    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.organization = self.cleaned_data['organization']
        if commit:
            user.save()
        return user

    

    

class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)





class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


# class BillingInfoForm(forms.ModelForm):
#     class Meta:
#         model = BillingInfo
#         fields = ['type', 'name', 'address', 'postal', 'country', 'vat_number']


class BillingInfoForm(forms.ModelForm):
    class Meta:
        model = BillingInfo
        fields = ['type', 'name', 'address', 'postal', 'country', 'vat_number']

        widgets = {
            'type': forms.Select(choices=[('Company', 'Company'), ('Personal', 'Personal')]),
            'name': forms.TextInput(attrs={'class': 'companyinput'}),
            'address': forms.TextInput(),
            'postal': forms.NumberInput(),
            'country': forms.Select(choices=[
                ('US', 'United States'), ('CA', 'Canada'), ('GB', 'United Kingdom'), ('AU', 'Australia'),
                ('DE', 'Germany'), ('FR', 'France'), ('IN', 'India'), ('CN', 'China'), ('JP', 'Japan'), ('BR', 'Brazil')
            ]),
            'vat_number': forms.NumberInput(),
        }