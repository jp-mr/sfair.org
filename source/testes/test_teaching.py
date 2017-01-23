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


class TeachingModelTests(TestCase):

    def test_class_create(self):
        obj = mommy.make(Class)
        self.assertIsInstance(obj, Class)
        self.assertEqual(obj.__str__(), obj.user.username)
        self.assertEqual(
                obj.get_markdown(),
                "<p>" + obj.notice_board + "</p>\n"
                )

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


class TeachingViewTests(TestCase):

    def setUp(self):
        self.user = mommy.make(User, username='usuario', password='senha123')
        self.course_code = mommy.make(CourseCode)
        self.class_obj = mommy.make(Class, user=self.user, course_code=self.course_code)
        self.client = Client()

    def test_teaching(self):
        PageDescription.objects.create(title='Teaching')
        response = self.client.get(reverse('teaching:teaching'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'teaching/teaching.html')
        self.assertTemplateUsed(response, 'javascript.html')

    # def test_student_modal_ajax_login(self):
    #     response = self.client.post(
    #             reverse('teaching:student-login'),
    #             {
    #                 'username': self.user.username,
    #                 'password': 'senha123'
    #             },
    #             HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    #             )
    #     self.assertEqual(response.status_code, 200)

    def test_student_area(self):
        self.client.force_login(User.objects.get_or_create(username=self.user.username)[0])
        response = self.client.get(reverse('teaching:student-area'),  {'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'teaching/student_area.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_student_area_redirect_to_login(self):
        response = self.client.get(reverse('teaching:student-area'))
        redirected_url = "{}?next={}".format(reverse('login'), reverse('teaching:student-area'))
        self.assertRedirects(response, redirected_url)

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
