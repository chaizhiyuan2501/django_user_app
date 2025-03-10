from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Todo
from .forms import TodoForm

class TodoCreateView(LoginRequiredMixin, CreateView):
    """ToDo 作成ビュー"""
    model = Todo
    form_class = TodoForm
    template_name = "todo/todo_create.html"
    success_message = "ToDo を作成しました。"

    def form_valid(self, form):
        """ログインユーザーを ToDo の user に設定"""
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        """作成後にリダイレクトするURL"""
        return reverse_lazy('todo_list')


class TodoListView(LoginRequiredMixin, ListView):
    """ToDo 一覧ビュー"""
    model = Todo
    template_name = "todo/todo_list.html"
    context_object_name = "todos"
    ordering = ['expire_date']  # 期限日順に並べる
    queryset = Todo.objects.none()  # 初期値として空のクエリセット

    def get_queryset(self):
        """ログインユーザーの ToDo のみを表示"""
        return Todo.objects.filter(user=self.request.user).order_by('expire_date')


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    """ToDo 更新ビュー"""
    model = Todo
    form_class = TodoForm
    template_name = "todo/todo_create.html.html"
    success_message = "ToDo を更新しました。"

    def get_queryset(self):
        """ログインユーザーが所有する ToDo のみ編集可能"""
        return Todo.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """フォームが有効な場合にメッセージを表示"""
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        """更新後にリダイレクトするURL"""
        return reverse_lazy('todo_list')


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    """ToDo 削除ビュー"""
    model = Todo
    template_name = "todo/todo_delete.html"
    success_url = reverse_lazy('todo_list')
    success_message = "ToDo を削除しました。"

    def get_queryset(self):
        """ログインユーザーが所有する ToDo のみ削除可能"""
        return Todo.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """削除成功時にメッセージを表示"""
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
