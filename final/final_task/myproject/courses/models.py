from django.db import models


class Course(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Lecture(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    topic = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course', related_query_name='course')

    def __str__(self):
        return self.name


class Homework(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    mark = models.IntegerField(blank=True, null=True)
    #user
    def __str__(self):
        return self.content

