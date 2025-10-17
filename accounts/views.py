from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, EmployerProfileForm
from django.contrib.auth.decorators import login_required
from .models import EmployerProfile





@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            role = form.cleaned_data.get("role")
            if role == "employer":
                # ensure employer profile exists and update with posted data
                profile = EmployerProfile.objects.get(user=user)
                profile.company_name = request.POST.get("company_name", "")
                profile.save()
            # auto login (optional)
            login(request, user)
            return redirect("job_feed")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pw = request.POST.get("password")
        user = authenticate(request, username=username, password=pw)
        if user:
            login(request, user)
            return redirect("job_feed")
        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
    return render(request, "accounts/login.html")
