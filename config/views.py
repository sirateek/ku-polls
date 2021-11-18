from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.urls import reverse


def signup(request):
    """Signup Form view and POST Handler."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect("/polls/")
        return render(request, 'registration/signup.html', {'form': form})
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
