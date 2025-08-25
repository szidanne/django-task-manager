from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Task, Status
from .forms import TaskForm


# Create your views here.
@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by("due_date", "-created_at")[
        :5
    ]
    context = {"tasks": tasks}
    return render(request, "tasks/index.html", context)


@login_required
def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    return render(request, "tasks/detail.html", {"task": task})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(reverse("tasks:detail", args=[task.id]))
    else:
        form = TaskForm(initial={"status": Status.PENDING})
    return render(request, "tasks/form.html", {"form": form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse("tasks:detail", args=[task.id]))
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/form.html", {"form": form, "task": task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect(reverse("tasks:index"))
    return render(request, "tasks/confirm_delete.html", {"task": task})
