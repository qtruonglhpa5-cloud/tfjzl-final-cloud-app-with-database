from django.urls import path
from . import views

urlpatterns = [
    # Submit exam for a specific course
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # Show exam result for a specific submission in a course
    path('course/<int:course_id>/submission/<int:submission_id>/result/', 
         views.show_exam_result, name='show_exam_result'),
]
