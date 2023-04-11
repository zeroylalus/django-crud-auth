
from django.urls import path
from task import views

urlpatterns = [

    path('', views.home, name='home'),

    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_tasks, name='create_tasks'),
    path('tasks/<int:id>', views.task_detail, name='tasks_detail'),
    path('tasks/<int:id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:id>/delete', views.delete_task, name='delete_task'),

    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
]