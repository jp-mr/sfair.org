from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import render

from core.models import PageDescription
from .models import Class, LectureNote


User = get_user_model()


def teaching(request):

    obj = PageDescription.objects.get(title='Teaching')
    template = "teaching/teaching.html"
    context = {
        'obj': obj
    }

    # Renderiza a página
    return render(request, template, context)


def student_login(request):
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        password = request.POST['password']
        if username == "":
            return HttpResponse('userEmptyError')
        if password == "":
            return HttpResponse('pwdEmptyError')
        user_qs = User.objects.filter(username=username)
        if not user_qs.exists():
            return HttpResponse('userDontExistError')
        user = authenticate(username=username, password=password)
        if user is not None:
            user_obj= User.objects.get(username=username)
            if user_obj.is_superuser or user_obj.is_staff:
                return HttpResponse('userNotAllowed')
            login(request=request, user=user)
            return HttpResponse(True)
        return HttpResponse('userPwdDontMatch')
    raise PermissionDenied


def student_logout(request):
    if request.method == 'POST' and request.is_ajax():
        logout(request=request)
        return HttpResponse(True)
    return Http404


@login_required
def student_area(request):

    user_id = request.user.id
    class_obj = Class.objects.select_related(
            'course_class',
            'course_code'
            ).get(user=user_id)
    lecture_notes = class_obj.lecture_notes.all()
    schedule = class_obj.date_set.all()
    course = class_obj.course_class
    course_title = class_obj.course_code.title
    course_description = class_obj.course_code.description
    duration = class_obj.duration
    period = class_obj.period
    notice_board = class_obj.notice_board

    for note in lecture_notes:
        if not note.upload.name:
            note.upload.name = 'noFile'

    template = "teaching/student_area.html"
    context = {
            'class_obj':class_obj,
            'lecture_notes': lecture_notes,
            'schedule': schedule,
            'course_title': course_title,
            'course_description': course_description,
            'duration': duration.capitalize(),
            'period': period.capitalize(),
            'course': course,
            'notice_board': notice_board,
            }

    # Renderiza a página
    return render(request, template, context)


def lecture_notes_download_couter(request):
    if request.method == 'POST' and request.is_ajax():
        lecture_note_id = request.POST.get('obj_id')
        lecture_note = LectureNote.objects.filter(id=lecture_note_id)
        lecture_note.update(download=F('download') + 1)
        return HttpResponse(True)
