from django import forms
from pagedown.widgets import AdminPagedownWidget

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
        'placeholder': 'Name'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Email'
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Message'
    }))


class PageDescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = PageDescription
        fields = "__all__"


class PublicationForm(forms.ModelForm):
    abstract = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Publication
        fields = "__all__"


# class ResearchPageDescriptionForm(forms.ModelForm):
#     description = forms.CharField(widget=AdminPagedownWidget())
# 
#     class Meta:
#         model = ResearchPageDescription
#         fields = "__all__"
# 
# 
# class TeachingPageDescriptionForm(forms.ModelForm):
#     description = forms.CharField(widget=AdminPagedownWidget())
# 
#     class Meta:
#         model = TeachingPageDescription
#         fields = "__all__"
# 
# 
# class ClusterPageDescriptionForm(forms.ModelForm):
#     description = forms.CharField(widget=AdminPagedownWidget())
# 
#     class Meta:
#         model = ClusterPageDescription
#         fields = "__all__"
# 
# 
# class FormationPageDescriptionForm(forms.ModelForm):
#     description = forms.CharField(widget=AdminPagedownWidget())
# 
#     class Meta:
#         model = FormationPageDescription
#         fields = "__all__"
