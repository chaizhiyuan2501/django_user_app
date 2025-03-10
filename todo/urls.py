from django.urls import path
from .views import TodoCreateView, TodoListView, TodoUpdateView, TodoDeleteView

app_name = "todo"

urlpatterns = [
    path('', TodoListView.as_view(), name='todo_list'),  # ToDo一覧
    path('create/', TodoCreateView.as_view(), name='todo_create'),  # ToDo作成
    path('<int:pk>/update/', TodoUpdateView.as_view(), name='todo_update'),  # ToDo更新
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='todo_delete'),  # ToDo削除
]
