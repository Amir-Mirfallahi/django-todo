from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.views import View
from django.contrib.auth import login, logout
from django.shortcuts import redirect


class LoginView(BaseLoginView):
    template_name = "accounts/login.html"
    form_class = UserLoginForm
    fields = "email", "password"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:todo_manage")


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:todo_manage")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy("todo:todo_manage"))
        return super(RegisterView, self).get(*args, **kwargs)


class LogoutView(View):
    """
    View for logging out a user.
    """

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, "accounts/logout.html")
