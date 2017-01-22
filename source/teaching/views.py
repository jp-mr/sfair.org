from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponse
from django.shortcuts import render


from core.models import PageDescription


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


def student_area(request):

    template = "teaching/student_area.html"
    context = {}

    # Renderiza a página
    return render(request, template, context)
