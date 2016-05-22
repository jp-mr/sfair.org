from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .forms import ContactForm


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
    #para o usuário
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
    title = "Contact"

    # [contat] Quando o usuário clicar no botão enviar,
    #o método da requicisão é avaliado
    if request.method == 'POST':

        # [contact] Uma instancia de form é criada com as informações do usuário
        form = ContactForm(request.POST or None)

        # [contact] Se as informações forem válidas
        if form.is_valid():

            # [contact] Extrai as informações da instancia de ContactForm
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')

            subject = "Contact - Sfair.org"

            # [contact] Atribui o email cadastrado no servidor SMTP
            from_email = settings.EMAIL_HOST_USER

            to_email = [from_email, ]
            contact_message = "%s: %s via %s" % (name, message, email)

            # Envia o email através do servidor SMTP
            send_mail(subject, contact_message, from_email, to_email, fail_silently=True)

            # Redireciona para a página principal adicionando '?sent=True' na URL
            # Vá para: função 'home'
            return redirect(reverse('core:home') + '?sent=True')

    form = ContactForm()

    context = {
        'title': title,
        'form': form,
    }

    return render(request, "forms.html", context)
