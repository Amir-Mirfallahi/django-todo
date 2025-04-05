from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm as BaseAuthenticationForm

User = get_user_model()

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "ایمیل خود را وارد کنید"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "رمز عبور خود را وارد کنید"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "تکرار رمز عبور خود را وارد کنید"}),
        }
        labels = {
            "email": "ایمیل",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",
        }
    email = forms.EmailField(error_messages={"required": "ایمیل الزامی است.", "invalid": "ایمیل معتبر نیست.", "unique": "ایمیل قبلا استفاده شده است.", "max_length": "ایمیل باید کمتر از 254 کاراکتر باشد."})
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput, error_messages={"required": "رمز عبور الزامی است.", "min_length": "رمز عبور باید حداقل 8 کاراکتر باشد."})
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput, error_messages={"required": "تکرار رمز عبور الزامی است.", "min_length": "تکرار رمز عبور باید حداقل 8 کاراکتر باشد."})

    def form_valid(self, form):
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        return user


class UserLoginForm(BaseAuthenticationForm):
    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "ایمیل خود را وارد کنید"}),
            "password": forms.PasswordInput(attrs={"placeholder": "رمز عبور خود را وارد کنید"}),
        }
        labels = {
            "email": "ایمیل",
            "password": "رمز عبور",
        }

