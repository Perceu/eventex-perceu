from django.test import TestCase

# Create your tests here.
class homeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')
    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_index(self):
        self.resp = self.client.get('/')
        self.assertTemplateUsed(self.resp, 'index.html')
