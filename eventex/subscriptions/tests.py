from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
# Create your tests here.
class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    
    def test_html(self):
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_crsftoken(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_form(self):
        from eventex.subscriptions.forms import SubscriptionForm
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = form = self.resp.context['form']
        self.assertListEqual(['name','cpf','email','phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(
            name="Perceu Bertoletti", 
            cpf="01234567890",
            email="perceubertoletti@gmail.com", 
            phone="54 99662 2121",
        )
        self.resp = self.client.post('/inscricao/',data)

    def test_post(self):
        self.assertEqual(302, self.resp.status_code)
    
    def test_send_subscribe_email(self):
        self.assertEqual(1,len(mail.outbox))

    def test_subscribe_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscribe_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, email.from_email)

    def test_subscribe_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'perceubertoletti@gmail.com']
        self.assertEqual(expect, email.to)
    
    def test_subscribe_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Perceu Bertoletti', email.body)
        self.assertIn('01234567890', email.body)
        self.assertIn('perceubertoletti@gmail.com', email.body)
        self.assertIn('54 99662 2121', email.body)

class SubscribeInvalidPost(TestCase):
    def setUp(self):
        data = dict()
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_form_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        data = dict(
            name="Perceu Bertoletti",
            cpf="01234567890",
            email="perceubertoletti@gmail.com",
            phone="54 99662 2121",
        )
        self.resp = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.resp,'Inscrição realizada com sucesso!')