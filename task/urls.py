
from django.urls import path
from task import views

urlpatterns = [

    path('', views.home, name='home'),

    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.create_tasks, name='create_tasks'),

    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
]