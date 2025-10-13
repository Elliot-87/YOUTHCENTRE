from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vacancy
from .forms import VacancyForm

@login_required
def post_create(request):
    if not request.user.profile.is_employer:
        return redirect('jobs:vacancy_list')
    form = VacancyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        vacancy = form.save(commit=False)
        vacancy.employer = request.user
        vacancy.save()
        return redirect('jobs:vacancy_detail', pk=vacancy.pk)
    return render(request, 'jobs/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk, employer=request.user)
    form = VacancyForm(request.POST or None, request.FILES or None, instance=vacancy)
    if form.is_valid():
        form.save()
        return redirect('jobs:vacancy_detail', pk=vacancy.pk)
    return render(request, 'jobs/post_form.html', {'form': form})
