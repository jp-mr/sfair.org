from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory

from django.contrib.auth import authenticate, login
from model_mommy import mommy

from core.models import PageDescription
from teaching.models import (
            Class,
            LectureNote,
            Date,
            CourseCode,
            Course,
            )


User = get_user_model()


class TeachingModelTest(TestCase):

    def test_class_create(self):
        obj = mommy.make(Class)
        self.assertIsInstance(obj, Class)
        self.assertEqual(obj.__str__(), obj.user.username)

    def test_lecture_note_create(self):
        obj = mommy.make(LectureNote)
        self.assertIsInstance(obj, LectureNote)
        self.assertEqual(obj.__str__(), obj.title)
        self.assertEqual(
                obj.get_markdown(),
                "<p>" + obj.lecture_note + "</p>\n"
                )

    def test_date_create(self):
        obj = mommy.make(Date)
        self.assertIsInstance(obj, Date)
        self.assertEqual(obj.__str__(), obj.description)

    def test_course_code_create(self):
        obj = mommy.make(CourseCode)
        self.assertIsInstance(obj, CourseCode)
        self.assertEqual(obj.__str__(), obj.code)

    def test_course_create(self):
        obj = mommy.make(Course)
        self.assertIsInstance(obj, Course)
        self.assertEqual(obj.__str__(), obj.course)


class TeachingViewTest(TestCase):

    def test_teaching(self):
        PageDescription.objects.create(title='Teaching')
        response = self.client.get(reverse('teaching:teaching'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'teaching/teaching.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_lecture_notes_download_counter(self):
        ln = mommy.make(LectureNote)
        ln = LectureNote.objects.first()
        self.assertEqual(ln.download, 0)
        cl = Client()
        response = cl.post(
                reverse('teaching:ln-download-counter'),
                {'obj_id': 1},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                )
        ln = LectureNote.objects.first()
        self.assertEqual(ln.download, 1)
