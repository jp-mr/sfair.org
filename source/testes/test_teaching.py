from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory

from django.contrib.auth import authenticate, login
from model_mommy import mommy

from core.models import PageDescription
from teaching.models import (
            Class,
            LectureNote,
            ClassLectureNote,
            Date,
            CourseCode,
            Course,
            )
from teaching.views import assign_attr_no_file

User = get_user_model()


class TeachingModelTests(TestCase):

    def test_class_create(self):
        obj = mommy.make(Class, notice_board="Texto de teste.")
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

    def test_class_lecture_note_create(self):
        class_obj = mommy.make(Class)
        lecture_note = mommy.make(LectureNote)
        cln = mommy.make(
                ClassLectureNote,
                class_user=class_obj,
                lecture_note=lecture_note
                )
        self.assertIsInstance(cln, ClassLectureNote)
        self.assertEqual(cln.__str__(), cln.lecture_note.title)

    def test_date_create(self):
        obj = mommy.make(Date)
        self.assertIsInstance(obj, Date)
        self.assertEqual(obj.__str__(), obj.description)

    def test_course_code_create(self):
        obj = mommy.make(CourseCode)
        self.assertIsInstance(obj, CourseCode)
        self.assertEqual(obj.__str__(), obj.code)
        self.assertEqual(
                obj.get_markdown(),
                "<p>" + obj.description + "</p>\n"
                )

    def test_course_create(self):
        obj = mommy.make(Course)
        self.assertIsInstance(obj, Course)
        self.assertEqual(obj.__str__(), obj.course)


class TeachingViewTests(TestCase):

    def setUp(self):
        self.user = mommy.make(User, username='usuario', password='senha123')
        self.course_code = mommy.make(CourseCode)
        self.class_obj = mommy.make(Class, user=self.user, course_code=self.course_code)
        self.lecture_note = mommy.make(LectureNote)
        self.client = Client()

    def test_teaching(self):
        PageDescription.objects.create(title='Teaching')
        response = self.client.get(reverse('teaching:teaching'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'teaching/teaching.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_lecture_note_assign_attr_no_file(self):
        mommy.make(
                ClassLectureNote,
                lecture_note=self.lecture_note,
                class_user=self.class_obj
                )
        cln = ClassLectureNote.objects.first()
        self.assertEqual(cln.lecture_note.upload.name, '')
        cln_parsed = assign_attr_no_file(cln)
        self.assertEqual(cln_parsed.lecture_note.upload.name, 'noFile')

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
        mommy.make(
                ClassLectureNote,
                lecture_note=self.lecture_note,
                class_user=self.class_obj
                )
        class_ln1 = ClassLectureNote.objects.first()
        data1 = {
            'cln_id': class_ln1.id,
            'ln_id': class_ln1.lecture_note.id,
            }
        self.assertEqual(self.lecture_note.download, 0)
        self.assertEqual(class_ln1.download, 0)
        cl = Client()
        response = cl.post(
                reverse('teaching:ln-download-counter'),
                data1,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                )
        class_ln1 = ClassLectureNote.objects.first()
        self.assertEqual(class_ln1.download, 1)
        self.assertEqual(class_ln1.lecture_note.download, 1)

        mommy.make(
                ClassLectureNote,
                lecture_note=self.lecture_note,
                class_user=self.class_obj,
                )
        class_ln2 = ClassLectureNote.objects.get(id=2)
        data2 = {
            'cln_id': class_ln2.id,
            'ln_id': class_ln2.lecture_note.id,
            }
        self.assertEqual(class_ln2.lecture_note.download, 1)
        self.assertEqual(class_ln2.download, 0)
        cl = Client()
        response = cl.post(
                reverse('teaching:ln-download-counter'),
                data2,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                )
        class_ln2 = ClassLectureNote.objects.get(id=2)
        self.assertEqual(class_ln2.download, 1)
        self.assertEqual(class_ln2.lecture_note.download, 2)

    def test_unauthorized401(self):
        response = self.client.get(reverse('teaching:unauthorized'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'teaching/status_401.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_student_logout(self):
        self.client.force_login(User.objects.get_or_create(username=self.user.username)[0])
        response = self.client.get(reverse('teaching:student-logout'))
        self.assertEqual(response.status_code, 200)
