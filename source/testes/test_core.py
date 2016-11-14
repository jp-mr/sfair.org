from django.test import TestCase
from model_mommy import mommy

from core.models import PageDescription, Publication


class CoreModelTest(TestCase):

    def test_PageDescription_create(self):
        pd = mommy.make(PageDescription)
        self.assertTrue(isinstance(pd, PageDescription))
        self.assertEqual(pd.__str__(), pd.title)
        self.assertEqual(
                pd.get_markdown(),
                "<p>" + pd.description + "</p>\n"
                )

    def test_Publication_create(self):
        pb = mommy.make(Publication)
        self.assertTrue(isinstance(pb, Publication))
        self.assertEqual(pb.__str__(), pb.title)
        self.assertEqual(
                pb.get_markdown(),
                "<p>" + pb.abstract + "</p>\n"
                )
