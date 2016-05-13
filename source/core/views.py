from django.shortcuts import render


def home(request):
    """
        [1] A função home renderiza a página principal

        'render' vai devolver uma resposta para o 'request'(requisição
        do navegador) renderizando o template 'home.html'

        'context' serve para passar valores de variáveis para exibir
        no template

        Vá para: template/home.html

    """

    context = {

        # envia o nome de uma classe CSS para exibir a img de fundo da home
        'img_background': "img-background",
    }

    return render(request, "home.html", context)


def contact(request):
    return render(request, "forms.html", {})
