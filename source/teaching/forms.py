from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from pagedown.widgets import AdminPagedownWidget

from core.utils import validate_pdf
from .models import Class, LectureNote, CourseCode


User = get_user_model()


class ClassForm(forms.ModelForm):
    notice_board = forms.CharField(
            widget=AdminPagedownWidget(),
            required=False,
            )

    class Meta:
        model = Class
        fields = [
            'user',
            'course_class',
            'course_code',
            'notice_board',
            # 'classroom',
            # 'class_time',
            'infobox_title',
            # 'duration',
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


class CourseCodeForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = CourseCode
        fields = [
            'title',
            'code',
            'description',
            'degree',
            ]


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

    def clean_username(self):
        username = self.cleaned_data['username']
        user_qs = User.objects.filter(username=username)
        if user_qs.exists() and user_qs.count() == 1:
            user = user_qs.first()
            if user.is_superuser or user.is_staff:
                raise forms.ValidationError("This user not allowed")
            else:
                return username
        raise forms.ValidationError("This user don't exist.")
