from rest_framework import serializers
from .models import Course, Lecture, Homework


class CourseSerializer(serializers.ModelSerializer):
    lectures = serializers.PrimaryKeyRelatedField(many=True, queryset=Lecture)

    class Meta:
        model = Course
        fields = ['name', 'lectures']

    # def create(self, validated_data):
    #     lectures_data = validated_data.pop('lecture')
    #     course = Course.objects.create(**validated_data)
    #     for lecture_data in lectures_data:
    #         Lecture.objects.create(course=course, **lecture_data)
    #     return course


class LectureSerializer(serializers.ModelSerializer):
    course = CourseSerializer

    class Meta:
        model = Lecture
        fields = ['name', 'topic', 'course']


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['name', 'content', 'mark']

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        return course
