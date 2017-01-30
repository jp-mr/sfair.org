from django import forms
from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory

from django.contrib.auth import get_user_model
from model_mommy import mommy
from reportlab.pdfgen import canvas
import os

from core.forms import ContactForm, PublicationForm
from core.models import PageDescription, Publication
from core.views import home
from core.utils import validate_pdf


User = get_user_model()

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
        self.assertTemplateUsed(response, 'research/research.html')
        self.assertTemplateUsed(response, 'javascript.html')

    def test_publication(self):
        for num in [1,1,2,3,4,4,5]:
            mommy.make(Publication, year=num)
        pb_qs = Publication.objects.all()
        pb_list = list(pb_qs)
        response = self.client.get(reverse('core:publications'))
        pb_context = list(response.context['pub_list'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'research/publications.html')
        self.assertTemplateUsed(response, 'javascript.html')
        self.assertEqual(response.context['years'], [5,4,3,2,1])
        self.assertEqual(pb_context, pb_list)
        self.assertEqual(len(pb_context), 7)
        for pb in pb_context:
            self.assertEqual(pb.upload.name, 'noFile')

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
        PageDescription.objects.create(title='Formation & CV')
        response = self.client.get(reverse('core:formation&CV'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'formation/formation.html')
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


# TODO: Tentar usar o Selenium
#
# class CoreFormTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#
#     def test_publication_valid_upload_file(self):
#         document = canvas.Canvas('example.pdf')
#         document.drawString(100,100, "Hello World")
#         document.showPage()
#         document.save()
#         uploaded_file =  UploadedFile(
#                 name="file.pdf",
#                 content_type='application/pdf',
#                 file=open('example.pdf', 'rb')
#                 )
#         data = {
#             'title': 'Título',
#             'author': 'Autor',
#             'journal': 'Revista',
#             'year': '2017',
#             'abstract': 'Loren ipsum',
#             'download': 0,
#             'upload': uploaded_file
#             }
#         #User.objects.create(username='michel', password='senha',
#         #        is_active=True, is_superuser=True)
#         #self.client.force_login(User.objects.get_or_create(username='michel')[0])
#         #url = '/admin/login/?next=/admin/core/publication/add/'
#         #response = self.client.get(url)
#         #r = self.client.post('/admin/core/publication/add/',
#         #        data=data,
#         #        file=uploaded_file
#         #        )
#         form = PublicationForm(data=data, files=uploaded_file)
#         #form.is_valid()
#         os.remove('example.pdf')
#
#      def test_publication_invalid_upload_file(self):
#          uploaded_file = SimpleUploadedFile(
#                  'text_file.pdf',
#                  'content need to be encoded'.encode()
#                  )
#          data = {
#              'title': 'Título',
#              'author': 'Autor',
#              'journal': 'Revista',
#              'year': '2017',
#              'abstract': 'Loren ipsum',
#              'download': 0,
#              'upload': uploaded_file
#              }
#          request = RequestFactory()
#          r = request.post('/admin/core/publication/add/', data=data)
#          print(r.parse_file_upload(META=r.META, post_data=data))
#          form = PublicationForm(r.POST)
#          form.clean()
#          result = form.is_valid()
#          self.assertFalse(result)


class ValidadePdfUploadTest(TestCase):

    def test_validate_pdf(self):
        document = canvas.Canvas('example.pdf')
        document.drawString(100,100, "Hello World")
        document.showPage()
        document.save()
        uploaded_file = UploadedFile(
                name="file.pdf",
                content_type='application/pdf',
                file=open('example.pdf', 'rb')
                )
        func_return = validate_pdf(uploaded_file)
        self.assertTrue(func_return)
        os.remove('example.pdf')

    def test_validate_another_type_file(self):
        """
            Retorna False porque e validação vai além da extensão do arquivo.
        """
        uploaded_file = SimpleUploadedFile(
                'text_file.pdf',
                'content need to be encoded'.encode()
                )
        output = validate_pdf(uploaded_file)
        self.assertFalse(output)
