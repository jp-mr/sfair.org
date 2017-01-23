from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render

from core.models import PageDescription
from .models import Class


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
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return HttpResponse(True)
        return Http404
    return Http404


@login_required
def student_area(request):

    user_id = request.user.id
    # TODO: usar prefetch_related
    class_obj = Class.objects.get(user=user_id)
    lecture_notes = class_obj.lecture_notes.all()
    schedule = class_obj.date_set.all()
    course_title = class_obj.course_code.title
    course_description = class_obj.course_code.description
    duration = class_obj.duration
    period = class_obj.period
    template = "teaching/student_area.html"
    context = {
            'lecture_notes': lecture_notes,
            'schedule': schedule,
            'course_title': course_title,
            'course_description': course_description,
            'duration': duration.capitalize(),
            'period': period.capitalize(),
            }

    # Renderiza a página
    return render(request, template, context)
