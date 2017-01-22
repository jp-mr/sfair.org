from django.contrib import admin

from .models import (
            Class,
            LectureNote,
            Date,
            CourseCode,
            Course,
            )
from .forms import LectureNoteForm


CLASS_INFO_FIELDS = [
        'user',
        'course_class',
        'course_code',
        'duration',
        'period'
        ]

LECTURES_NOTES_FIELDS = ['lecture_notes']


class LectureNoteModelAdmin(admin.ModelAdmin):

    form = LectureNoteForm

    search_fields = ['title', 'lecture_note']
    readonly_fields = ['download', 'timestamp', 'updated']
    actions = ['delete_selected']
    list_display = [
            'title',
            'download',
            'updated',
            'timestamp'
            ]


class DateInline(admin.TabularInline):

    actions = ['delete_selected']

    model = Date
    extra = 0


class CourseCodeModelAdmin(admin.ModelAdmin):

    actions = ['delete_selected']
    list_display = [
            'title',
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

    list_display = (
            'user',
            'course_class',
            'course_code',
            'duration',
            'period',
            )

    filter_horizontal = ['lecture_notes',]

    list_select_related = (
            'user',
            'course_class',
            'course_code',
            )

    fieldsets = [
            ('CLASS INFO', {'fields': CLASS_INFO_FIELDS}),
            ('LECTURES NOTES', {'fields': LECTURES_NOTES_FIELDS}),
            ]

    class Meta:
        model = Class


admin.site.register(Class, ClassModelAdmin)
admin.site.register(LectureNote, LectureNoteModelAdmin)
admin.site.register(CourseCode, CourseCodeModelAdmin)
admin.site.register(Course, CourseModelAdmin)
