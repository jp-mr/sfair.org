from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe

from markdown_deux import markdown


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
    notice_board = models.TextField()
    duration = models.CharField(max_length=10, choices=DURATION, blank=True)
    period = models.CharField(max_length=15, choices=PERIOD, blank=True)
    lecture_notes = models.ManyToManyField('LectureNote', blank=True)

    class Meta:
        verbose_name_plural = "classes"

    def __str__(self):
        return self.user.username

    def get_markdown(self):
        notice_board = self.notice_board
        markdown_text = markdown(notice_board)
        return mark_safe(markdown_text)


class LectureNote(models.Model):
    title = models.CharField(max_length=500)
    lecture_note = models.TextField()
    upload = models.FileField(
            upload_to='lectures-notes',
            max_length=100,
            blank=True
            )
    download = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_markdown(self):
        lecture_note = self.lecture_note
        markdown_text = markdown(lecture_note)
        return mark_safe(markdown_text)


class Date(models.Model):
    class_date = models.ForeignKey(Class, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    date = models.DateField()

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['date']


DEGREES = (
        ('graduation','Graduation'),
        ('master','Master'),
        ('doctoral','Doctoral'),
        )


class CourseCode(models.Model):
    title = models.CharField(max_length=140)
    code = models.CharField(max_length=25)
    description = models.TextField()
    degree = models.CharField(max_length=10, choices=DEGREES, blank=True)

    def __str__(self):
        return self.code


class Course(models.Model):
    course = models.CharField(max_length=80)

    def __str__(self):
        return self.course
