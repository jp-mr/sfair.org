from django import forms
from pagedown.widgets import AdminPagedownWidget
import magic

from .models import PageDescription, Publication


class ContactForm(forms.Form):
    """
    [contact] Os campos do formulário são declarados nessa classe e uma
    instancia é criada na 'view.py'

    O widget 'TextInput' implementa um entrada de texto de uma única linha,
    'Textarea' implementa uma entrada de texto de multiplas linhas
    'attrs' são atributos passado para a tag no tamplete
    'placeholder' é um texto que serve o usuário dentro da caixa de texto e
    some quando o usuário começa a digitar

    Vá para: views.py

    """
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Name',
        'required': True,
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'pattern': "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{1,6})",
        'required': True,
        'title':"Example:\nemail@domain.org\nemail@domain.com\nemail@domain.com.br"
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Subject',
        'required': True,
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Message',
        'required': True,
    }))


class PageDescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = PageDescription
        fields = [
            'title',
            'description',
            ]

class PublicationForm(forms.ModelForm):
    abstract = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Publication
        fields = [
            'title',
            'author',
            'journal',
            'year',
            'abstract',
            'upload',
            'download',
            ]

    def clean(self):
        # [publications] Sobrecreve o método 'clean' que é chamado para fazer
        # a validação das informações enviadas em um formulário.
        cleaned_data = super(PublicationForm, self).clean()
        uploaded_file = self.cleaned_data["upload"]
        if uploaded_file:
            # [publications] Utilizando uma biblioteca de terceiros, verifica
            # se o arquivo carregado é um PDF
            supported_types = ['application/pdf',]
            mime_type = magic.from_buffer(uploaded_file.file.read(1024), mime=True)
            uploaded_file.file.seek(0)
            if mime_type not in supported_types:
                msg = 'Unsupported file type. Just PDF are allowed.'
                self.add_error('upload', msg)
        return cleaned_data
