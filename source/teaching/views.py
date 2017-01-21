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



