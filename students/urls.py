from .views import students, update_students
from django.urls import path 

urlpatterns = [
    path('', students, name='students'),
    path('<str:student_id>/', update_students, name='update-students'),
]