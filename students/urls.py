from .views import students, update_students, faculty, guardian
from django.urls import path 

urlpatterns = [
    path('', students, name='students'),
    path('faculty/', faculty, name='faculty'),
    path('guardian/', guardian, name='guardian'),
    path('<str:student_id>/', update_students, name='update-students'),
]