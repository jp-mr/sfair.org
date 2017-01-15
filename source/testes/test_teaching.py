from django.test import TestCase, Client, RequestFactory
from model_mommy import mommy

from teaching.models import (
            Class,
            LectureNote,
            Date,
            CourseCode,
            Course,
            )


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


