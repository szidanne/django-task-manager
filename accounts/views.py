from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login


def home(request):
    # Root page: redirect authed users to tasks, show welcome to guests
    if request.user.is_authenticated:
        return redirect("tasks:index")
    return render(request, "home.html")


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("tasks:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect(self.get_success_url())
