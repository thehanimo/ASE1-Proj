from django.test import TestCase

# Create your tests here.
from django.test.client import Client
from django.urls import reverse


class UsersListViewTest(TestCase):

#views
    def test_view_uses_correct_template_cart_add(self):
        response = self.client.get(reverse('cart:cart_add'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_cart_remove(self):
        response = self.client.get(reverse('cart:cart_remove'))
        self.assertEqual(response.status_code, 302)