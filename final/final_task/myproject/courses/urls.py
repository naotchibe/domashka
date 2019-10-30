from django.urls import path, include
from .views import CreateCoursesApiView, RUDCoursesApiView, CreateLectureApiView, ListCoursesApiView, ListLecturesApiView


urlpatterns = [
    path('', ListCoursesApiView.as_view(), name='list_courses'),
    path('create/', CreateCoursesApiView.as_view(), name='create_course'),
    path('<int:pk>/', RUDCoursesApiView.as_view(), name='rud_course'),
    path('lectures/', ListLecturesApiView.as_view(), name='list_lectures'),
    path('lectures/<int:pk>/', ListLecturesApiView.as_view(), name='rud_lecture'),
    path('lectures/create/', CreateLectureApiView.as_view(), name='create_lecture')

]