from django.contrib import admin

from .models import (
            Class,
            LectureNote,
            ClassLectureNote,
            Date,
            CourseCode,
            Course,
            )
from .forms import ClassForm, LectureNoteForm, CourseCodeForm


CLASS_INFO_FIELDS = [
        'user',
        'course_class',
        'course_code',
        'classroom',
        'class_time',
        'duration',
        'infobox_title',
        ]

NOTICE_BOARD_FIELDS = ['notice_board']


class LectureNoteModelAdmin(admin.ModelAdmin):

    form = LectureNoteForm

    search_fields = ['title', 'lecture_note']
    readonly_fields = ['timestamp', 'updated']
    actions = ['delete_selected']
    list_display = [
            'title',
            'download',
            'updated',
            'timestamp'
            ]


class ClassLectureNoteInline(admin.TabularInline):

    actions = ['delete_selected']
    model = ClassLectureNote
    extra = 0


class DateInline(admin.TabularInline):

    actions = ['delete_selected']

    model = Date
    extra = 0


class CourseCodeModelAdmin(admin.ModelAdmin):

    form = CourseCodeForm
    actions = ['delete_selected']
    list_display = [
            'title',
            'code',
            'degree',
            ]


class CourseModelAdmin(admin.ModelAdmin):

    actions = ['delete_selected']

    class Meta:
        model = Course


class ClassModelAdmin(admin.ModelAdmin):

    form = ClassForm

    actions = ['delete_selected']

    inlines = [
            ClassLectureNoteInline,
            DateInline,
            ]

    list_display = (
            'user',
            'course_class',
            'course_code',
            'classroom',
            'class_time',
            )

    list_select_related = (
            'user',
            'course_class',
            'course_code',
            )

    fieldsets = [
            ('CLASS INFO', {'fields': CLASS_INFO_FIELDS}),
            ('NOTICE BOARD', {'fields': NOTICE_BOARD_FIELDS}),
            ]


admin.site.register(Class, ClassModelAdmin)
admin.site.register(LectureNote, LectureNoteModelAdmin)
admin.site.register(CourseCode, CourseCodeModelAdmin)
admin.site.register(Course, CourseModelAdmin)
