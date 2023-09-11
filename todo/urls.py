from django.urls import path
from todo import views as todo_views

urlpatterns = [
    path("tasks/", todo_views.TasksAPIView.as_view()),
    path("tasks/<uuid:task_id>/", todo_views.TaskAPIView.as_view()),
    path("tasks/<uuid:task_id>/toggle/", todo_views.ToggleTaskAPIView.as_view()),
]
