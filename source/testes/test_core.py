from django import forms
from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from model_mommy import mommy

from core.forms import ContactForm
from core.models import PageDescription, Publication
from core.views import home
from core.utils import validate_pdf



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
        response = self.client.get(reverse('core:home'), {'sent': True})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'javascript.html')
        self.assertEqual(response.context['message_sent'], 'message_sent')

    def test_research(self):
        PageDescription.objects.create(title='Research')
        response = self.client.get(reverse('core:research'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'research.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_publication(self):
        for num in [1,1,2,3,4,4,5]:
            pb = mommy.make(Publication)
            pb.year = num
            pb.save()
        pb_qs = Publication.objects.all()
        pb_list = list(pb_qs)
        response = self.client.get(reverse('core:publications'))
        pb_context = list(response.context['pub_list'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'publications.html')
        self.assertTemplateUsed(response, 'javascript.html')
        self.assertEqual(response.context['years'], [5,4,3,2,1])
        self.assertEqual(pb_context, pb_list)
        self.assertEqual(pb_context[0].upload.name, 'noFile')

    def test_publication_download_counter(self):
        pb = mommy.make(Publication)
        pub = Publication.objects.first()
        self.assertEqual(pub.download, 0)
        cl = Client()
        response = cl.post(
                reverse('core:publications'),
                {'pub_id': 1},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                )
        pub = Publication.objects.first()
        self.assertEqual(pub.download, 1)

    def test_formation(self):
        PageDescription.objects.create(title='Formation')
        response = self.client.get(reverse('core:formation&CV'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'formation.html')
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
        settings.EMAIL_DESTINY = 'another_destiny@email.com'
        response = self.client.post(reverse('core:contact'), self.valid_post_email)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, 'contact@sfair.org')
        self.assertEqual(email.subject, 'TESTE')
        self.assertEqual(
                email.body,
                'Michel Rodrigues <email@teste.com> \n\n 1, 2... TESTANDO!')
        self.assertEqual(
                email.to,
                ['contact@sfair.org', 'another_destiny@email.com']
                )
        self.assertEqual(email.reply_to, ['email@teste.com'])


class ValidadePdfUploadTest(TestCase):
    #pb = mommy.make(Publication)
    #pb.file_field = SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!')
    #pb.save()

    def test_validate_pdf(self):
        uploaded_file = SimpleUploadedFile(
                'best_file_eva.txt',
                'these are the file contents!'
                )
        func_return = validate_pdf(uploaded_file)
        self.assertFalse(func_return)
