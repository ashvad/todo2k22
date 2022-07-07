from django.urls import path
from todoapp import views

urlpatterns = [
    path("todos", views.TodoCreateView.as_view())
]
