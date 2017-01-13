from django.contrib import admin

from .models import (
            Class,
            LectureNote,
            Date,
            CourseCode,
            Course,
            )


class LectureNoteModelAdmin(admin.ModelAdmin):

    actions = ['delete_selected']
    list_display = [
            'title',
            'download',
            'updated',
            'timestamp'
            ]

    class Meta:
        model = LectureNote


class DateInline(admin.TabularInline):

    actions = ['delete_selected']

    model = Date
    extra = 0


class CourseCodeModelAdmin(admin.ModelAdmin):

    actions = ['delete_selected']
    list_display = [
            'code',
            'degree',
            ]

    class Meta:
        model = CourseCode


class CourseModelAdmin(admin.ModelAdmin):

    actions = ['delete_selected']

    class Meta:
        model = Course


class ClassModelAdmin(admin.ModelAdmin):

    actions = ['delete_selected']

    inlines = [
            DateInline,
            ]

    list_display = [
            'user',
            'course_class',
            'course_code',
            'duration',
            'period',
            ]

    class Meta:
        model = Class


admin.site.register(Class, ClassModelAdmin)
admin.site.register(LectureNote, LectureNoteModelAdmin)
admin.site.register(CourseCode, CourseCodeModelAdmin)
admin.site.register(Course, CourseModelAdmin)
