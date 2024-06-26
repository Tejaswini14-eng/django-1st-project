from django import forms
from .models import product
from django.contrib.auth.models import User

class AddProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['prod_name','description','manufacturer','price','category','isAvailable','image']
        exclude = []

class updateproductform(forms.ModelForm):
    class Meta:
        model = product
        fields = ['prod_name','description','manufacturer','price','category','isAvailable']
        exclude = []

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    confirmPassword = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        feilds = ['first_name','last_name','email','username','password','confirmPassword']
        exclude = ['is_superuser', 'is_staff', 'is_active', 'date_joined']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget = forms.PasswordInput)


class updateuserform(forms.ModelForm):
    class Meta:
        model = User
        feilds = ['first_name','last_name','email','username','is_staff']
        exclude = ['is_superuser','is_active','date_joined','password','confirmPassword','last_ogin' 'groups']

