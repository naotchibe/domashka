from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from .models import Course, Lecture, Homework
from .serializer import CourseSerializer, LectureSerializer, HomeworkSerializer
from rest_framework import serializers


class ListCoursesApiView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ListLecturesApiView(ListAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()


class RUDLecturesApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()


class RUDCoursesApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get(self, request, *args, **kwargs):
        print(args)
        id_course = request.pk
        course = Course.objects.get(pk=id_course)
        data = CourseSerializer(course).data
        return data


class CreateCoursesApiView(CreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CreateLectureApiView(CreateAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()




