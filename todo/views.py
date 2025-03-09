from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Todo


class TodoCreateView(LoginRequiredMixin, CreateView):
    pass


class TodoListView(LoginRequiredMixin, ListView):
    pass


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    pass


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    pass
