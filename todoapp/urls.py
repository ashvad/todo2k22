from django.urls import path
from todoapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("vtodos", views.TodoViewsets, basename="vtodos")
router.register("mvtodos",views.TodoModelViewset,basename="mvtodos")
router.register("accounts/signup",views.UserViewsets,basename="usersviewset")

urlpatterns = [
    path('todos', views.TodoCreateView.as_view()),
    path('todos/<int:id>', views.TodoDetail.as_view()),
    path('mtodos', views.TodoMisxinList.as_view()),
    path('mtodos/<int:id>', views.TodoMixinDetail.as_view()),
    path('accounts/login',views.SigninView.as_view())
]+router.urls
