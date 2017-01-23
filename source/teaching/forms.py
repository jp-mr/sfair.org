from django import forms
from django.contrib.auth.forms import AuthenticationForm
from pagedown.widgets import AdminPagedownWidget

from core.utils import validate_pdf
from .models import Class, LectureNote


class ClassForm(forms.ModelForm):
    notice_board = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Class
        fields = [
            'user',
            'course_class',
            'course_code',
            'duration',
            'period',
            'notice_board',
            'lecture_notes',
            ]


class LectureNoteForm(forms.ModelForm):
    lecture_note = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = LectureNote
        fields = [
            'title',
            'lecture_note',
            'upload',
            'download',
            ]
            # XXX: Se esses campos forem passada dentro da lista levanta uma
            # exceção. Entretanto, se não forem adicionados a lista, ainda sim
            # são exibidos no admin.
            #
            # django.core.exceptions.FieldError:
            # Unknown field(s)(timestamp, updated) specified for LectureNote
            #
            # 'timestamp',
            # 'updated',


    def clean(self):
        cleaned_data = super(LectureNoteForm, self).clean()
        uploaded_file = self.cleaned_data["upload"]
        if uploaded_file:
            if not validate_pdf(uploaded_file):
                msg = 'Unsupported file type. Just PDF are allowed.'
                self.add_error('upload', msg)
        return cleaned_data


class LoginForm(AuthenticationForm):

    username = forms.CharField(
            label="Username",
            max_length=30,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'name': 'username',
                    'placeholder': 'Username',
                    }
                )
            )

    password = forms.CharField(
            label="Password",
            max_length=30,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'password',
                    'name': 'password',
                    'placeholder': 'Password',
                    }
                )
            )
