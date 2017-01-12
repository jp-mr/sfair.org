from django import forms
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy

from core.forms import ContactForm
from core.models import PageDescription, Publication
from core.views import home



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


class CoreViewTest(TestCase):

    def setUp(self):
        self.valid_post_email = {
                'name': 'Michel Rodrigues',
                'email': 'email@teste.com',
                'subject': 'TESTE',
                'message': '1, 2... TESTANDO!',
                }

    def test_home(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_contact(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'forms.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_has_form_on_context(self):
        response = self.client.get(reverse('core:contact'))
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertTrue(response.context['title'], 'Contact')

    def test_contact_email_field_pattern(self):
        self.assertFieldOutput(
                forms.EmailField,
                {'a@a.com': 'a@a.com'},
                {'aaa': ['Enter a valid email address.']}
                )

    def test_send_contact_email(self):
        self.assertEquals(len(mail.outbox), 0)
        response = self.client.post(reverse('core:contact'), self.valid_post_email)
        self.assertEquals(len(mail.outbox), 1)

    def test_content_contact_email(self):
        response = self.client.post(reverse('core:contact'), self.valid_post_email)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, 'contact@sfair.org')
        self.assertEqual(email.subject, 'TESTE')
        self.assertEqual(
                email.body,
                'Michel Rodrigues <email@teste.com> \n\n 1, 2... TESTANDO!')
        self.assertEqual(email.to, ['contact@sfair.org'])
        self.assertEqual(email.reply_to, ['email@teste.com'])
