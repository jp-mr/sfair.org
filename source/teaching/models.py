from django.conf import settings
from django.db import models


DURATION = (
        ('sem1', '1º Semester'),
        ('sem2', '2º Semester'),
        ('annual','Annual')
        )

PERIOD = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('nocturnal', 'Nocturnal'),
        )


class Class(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            limit_choices_to={'is_staff': False, 'is_superuser': False}
            )
    lecture_notes = models.ManyToManyField('LectureNote', blank=True)
    course_class = models.ForeignKey(
            'Course',
            on_delete=models.SET_NULL,
            null=True,
            )
    course_code = models.ForeignKey(
            'CourseCode',
            on_delete=models.SET_NULL,
            null=True,
            )
    duration = models.CharField(max_length=10, choices=DURATION, blank=True)
    period = models.CharField(max_length=15, choices=PERIOD, blank=True)

    def __str__(self):
        return self.user.username


class LectureNote(models.Model):
    title = models.CharField(max_length=300)
    lecture_note = models.TextField()
    upload = models.FileField(
            upload_to='lectures-notes',
            max_length=100,
            blank=True
            )
    download = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


class Date(models.Model):
    class_date = models.ForeignKey(Class, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    date = models.DateField()

    def __str__(self):
        return self.description


DEGREES = (
        ('graduation','Graduation'),
        ('master','Master'),
        ('doctoral','Doctoral'),
        )


class CourseCode(models.Model):
    code = models.CharField(max_length=20)
    description = models.TextField()
    degree = models.CharField(max_length=10, choices=DEGREES, blank=True)

    def __str__(self):
        return self.code


class Course(models.Model):
    course = models.CharField(max_length=80)

    def __str__(self):
        return self.course
