from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import render

from core.models import PageDescription
from core.utils import check_student_user, assign_attr_no_file
from .models import Class, LectureNote, ClassLectureNote


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
        username = request.POST.get('username')
        password = request.POST.get('password')
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
    logout(request=request)
    return HttpResponse(request.user)


@login_required
@user_passes_test(
        check_student_user,
        login_url="teaching:unauthorized",
        redirect_field_name=''
        )
def student_area(request):

    user_id = request.user.id
    class_obj = Class.objects.select_related(
            'course_class',
            'course_code'
            ).get(user=user_id)
    class_lecture_notes = class_obj.classlecturenote_set.all()
    schedule = class_obj.date_set.all()
    course = class_obj.course_class
    course_title = class_obj.course_code.title
    course_description = class_obj.course_code
    # duration = class_obj.duration
    infobox_title = class_obj.infobox_title
    # classroom = class_obj.classroom
    # class_time = class_obj.class_time
    notice_board = class_obj.notice_board

    cln = [assign_attr_no_file(note) for note in class_lecture_notes]

    template = "teaching/student_area.html"
    context = {
            'class_obj': class_obj,
            'class_lecture_notes': cln,
            'schedule': schedule,
            'course_title': course_title,
            'course_description': course_description,
            # 'duration': duration.capitalize(),
            'course': course,
            'notice_board': notice_board,
            'infobox_title': infobox_title,
            # 'classroom': classroom,
            # 'class_time': class_time,
            }

    return render(request, template, context)


def unauthorized401(request):
    template = "teaching/status_401.html"
    return render(request, template, {})


def lecture_notes_download_couter(request):
    if request.method == 'POST' and request.is_ajax():
        cln_id = request.POST.get('cln_id')
        ln_id = request.POST.get('ln_id')
        ClassLectureNote.objects.filter(id=cln_id).update(download = F('download') + 1)
        LectureNote.objects.filter(id=ln_id).update(download = F('download') + 1)
        return HttpResponse(True)
