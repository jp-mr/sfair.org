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

        'context' serve para passar valores de variáveis para exibir
        no template

        Vá para: template/home.html

    """
    msg_sent = request.GET.get('sent', False)

    context = {

        # [home ]envia o nome de uma classe CSS para exibir a img
        # de fundo da home
        'img_background': "img-background",
    }

    if msg_sent:
        context['message_sent'] = 'message_sent'   

    return render(request, "home.html", context)


def contact(request):

    # TODO: pesquisar o ataque "email header injection" e implementar
    # uma solução se for o caso

    title = "Contact"

    if request.method == 'POST':

        form = ContactForm(request.POST or None)
    
        if form.is_valid():
            
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            subject = "Contact - Sfair.org"
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, ]
            contact_message = "%s: %s via %s" % (name, message, email)
            send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
    
            return redirect(reverse('core:home') + '?sent=True')

    form = ContactForm()

    context = {
        'title': title,
        'form': form,
    }

    return render(request, "forms.html", context)
