from django.conf import settings
from django.core.mail import EmailMessage  # send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import render, redirect

from .forms import ContactForm
from .models import Publication, PageDescription

import os


def home(request):
    """
        [home] A função home renderiza a página principal

        'render' vai devolver uma resposta para o 'request'(requisição
        do navegador) renderizando o template 'home.html'

        'context' serve para passar valores de variáveis que
        podem ser usadas no template

        Vá para: template/home.html

    """
    context = {

        # [home] envia o nome de uma classe CSS para exibir a img
        # de fundo da home
        'img_background': "img-background",
    }

    # [contact] Atribui o valor 'True' capturado da URL
    # após o redirecionamento da página de contato
    msg_sent = request.GET.get('sent', False)

    # [contact] Adiciona uma chave/valor para ser enviada ao template
    # através do contexto para exibir uma mensagem de confirmação
    # para o usuário
    # Vá para: template/home.html
    if msg_sent:
        context['message_sent'] = 'message_sent'

    return render(request, "home.html", context)


def contact(request):

    # TODO: pesquisar o ataque "email header injection" e implementar
    # uma solução se for o caso

    """
    [contact] A função contact renderiza a página de contatos
    um formulário é passado por meio do contexto.
    Vá para: forms.py

    """

    # [contact] Título que será enviado para o template através do contexto
    title = 'Contact'


    # [contat] Quando o usuário clicar no botão enviar,
    # o método da requicisão é avaliado
    if request.method == 'POST':

        # [contact] Uma instancia de form é criada com as informações
        # do usuário
        form = ContactForm(request.POST or None)

        # [contact] Se as informações forem válidas
        if form.is_valid():

            # [contact] Extrai as informações da instancia de ContactForm
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            subject = form.cleaned_data.get('subject')

            # [contact] Atribui o email cadastrado no servidor SMTP
            from_email = settings.EMAIL_HOST_USER

            to_email = [from_email, ]

            # [contact] Se a variável EMAIL_DESTINY, no arquivo de
            # configuração do django, não for "False", adiciona o seu valor a
            # lista de destinatários
            if settings.EMAIL_DESTINY:
                to_email += [settings.EMAIL_DESTINY]

            contact_message = "%s <%s> \n\n %s" % (name, email, message)

            # send_mail(
            #     subject,
            #     contact_message,
            #     from_email,
            #     to_email,
            #     reply_to=[email],
            #     fail_silently=False
            # )

            # XXX TODO: Pesquisar se é possível tratar a exceção quando
            #           o envio do email falhar. Essa exceção só é
            #           levantada quando a variável "fail_silently"
            #           for igual a "False".

            # [contact] Envia o email através do servidor SMTP
            msg = EmailMessage(
                    subject,
                    contact_message,
                    from_email,
                    to_email,
                    reply_to=[email],
                    )

            msg.send(fail_silently=False)

            # [contact] Redireciona para a página principal
            # adicionando '?sent=True' na URL
            # Vá para: função 'home'
            return redirect(reverse('core:home') + '?sent=True')

    # Instancia um formulário em branco
    form = ContactForm()

    # Contexto que será enviado para o template para exibir um título
    # para a página e o formulário em branco
    context = {
        'title': title,
        'form': form,
    }

    # Renderiza a página
    return render(request, "forms.html", context)


def formation(request):

    obj_qs = PageDescription.objects.filter(title__icontains='Formation')
    obj = obj_qs.first()

    context = {
        'obj': obj
    }

    # Renderiza a página
    return render(request, "formation.html", context)


def research(request):

    obj = PageDescription.objects.get(title='Research')

    context = {
        'obj': obj
    }

    # Renderiza a página
    return render(request, "research.html", context)


def publications(request):

    # [publications] Se o método de requisição for POST e AJAX
    # (após clicar em 'Download'), é capturado o ID do artigo
    # e usado para buscá-lo no banco de dados. Após, é somando 1
    # ao valor do campo 'counter'.
    # Obs: a paǵina não é atualizada.

    if request.method == 'POST' and request.is_ajax():
        publication_id = request.POST.get('pub_id')

        # [publications] O método filter retorna um objeto Queryset com todos
        # os objetos que batem com a cláusula passada como argumento. Como o
        # campo 'id' gerado automaticamento pelo Django é sempre único,
        # Queryset conterá sempre apenas um objeto.
        # O método '.update()' do objeto Queryset executa a mesma operação do
        # método '.save()' do objeto Model. A função F() passada como
        # argumento para o método '.update()' faz com que a operação de
        # incremento seja executada diretamente no banco de dados através de
        # uma expressão SQL, sem que o Python tenha que carregar qualquer
        # valor em sua memória ou executar a operação de soma.
        publication = Publication.objects.filter(id=publication_id)
        publication.update(download=F('download') + 1)

        # [publications](Esse bloco de código foi subtítuido pela 
        # linha acima.)
        # O método 'get' busca no banco de dados objeto com
        # o ID passado pela requisição e retorna esse objeto.
        # publication = Publication.objects.get(id=publication_id)
        # publication.download += 1
        # publication.save()


    # [publications] Se o método de requisição for GET, todos os artigos
    # serão trazidos do banco de dados e separados em grupos pelo paginador

    # [publications] Captura todos os artigos do banco de dados
    # publications = Publication.objects.all()
    queryset = Publication.objects.all()

    #for p in publications:
    #    if not p.upload.name:
    #        p.upload.name = 'noFile'

    # [publications] Função que implementa a pagiçãoo
    # paginator = Paginator(publications, 6)  # Exibe 6 artigos por página

    # [publications] Cria uma lista com os número das páginas.
    # Será passado como contexto para exibir os números nos botões
    # do paginador
    # l = []
    # for page in paginator.page_range:
    #     l.append(page)

    # [publications] Captura o valor da variável page no cabeçalho
    # da requisição. Esse valor só existe a partir da segunda página.
    # Também é passado no contexto para determinar qual botão será
    # destacado na páginação
    # page_request_var = 'page'
    # page = request.GET.get(page_request_var)

    # try:
    #     # [publications] Se a váriavel 'page'for 'None', levanta uma exceção,
    #     # senão 'queryset' recebe os artigos que devem ser exibidos ná pagina
    #     # requisitada pelo 'request'
    #     queryset = paginator.page(page)

    # except PageNotAnInteger:
    #     # [publications] Se page não é um inteiro, retorna a primeira página
    #     queryset = paginator.page(1)

    # except EmptyPage:
    #     queryset = paginator.page(paginator.num_pages)

    # [publications] Cria uma lista com os anos das publicações. Se algum ano
    # já estiver na lista, não é adicionado novamente a lista.
    # Verifica se cada publicação tem um arquivo PDF associado, caso não
    # tenha, atribui uma string que será usada em 'publications.html' num
    # bloco 'if' para não exibir o link de download
    years = []
    for qs in queryset:
        if not qs.year in years:
            years.append(qs.year)
        if not qs.upload.name:
            qs.upload.name = 'noFile'

    context = {
        'pub_list': queryset,
        'years': years,
        # 'page_request_var': page_request_var,
        # 'list': l,
        # 'page': page,
    }

    # [publications] Renderiza a página
    # Vá para: templates/publications.html
    return render(request, "publications.html", context)
