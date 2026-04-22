from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Register hote hi login kar do
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})

# 1. Task List dikhane aur Naya Task add karne ke liye
@login_required(login_url='login')
def task_list(request):
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            # Task ko logged-in user ke saath map kar rahe hain
            Task.objects.create(user=request.user, title=title)
        return redirect('task_list')

    # Sirf wahi tasks dikhao jo is user ke hain
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todo/index.html', {'tasks': tasks})

# 2. Task Delete karne ke liye
@login_required(login_url='login')
def delete_task(request, pk):
    # Security check: User sirf apna hi task delete kar paye
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return redirect('task_list')

# 3. Task ko Done/Pending mark karne ke liye
@login_required(login_url='login')
def toggle_task(request, pk):
    # Security check: User sirf apna hi task toggle kar paye
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')