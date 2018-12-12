
from django.test import TestCase
#from userAuth import User
# Create your tests here.
from django.test.client import Client
from django.urls import reverse

class UsersListViewTest(TestCase):
    #
    # @classmethod
    # def setUpTestData(cls):
    #     cls.client = Client()
    #     cls.user = User.objects.create_user(email='vhimareddy19997@gmail.com', email_verified=True,user_type=2)



    def test_view_uses_correct_template_executiveDetailsView(self):
        response = self.client.get(reverse('executive:register'))
        self.assertEqual(response.status_code, 302)


    def test_view_uses_correct_template_viewprofile(self):
        response = self.client.get(reverse('executive:home'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_all_orders(self):
        response = self.client.get(reverse('executive:viewprofile'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_order(self):
        response = self.client.get(reverse('executive:agentslist'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_incomingorders(self):
        response = self.client.get(reverse('executive:editagent'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_assignedorders(self):
        response = self.client.get(reverse('executive:deleteagent'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_completedorders(self):
        response = self.client.get(reverse('executive:create_category'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_cancledorders(self):
        response = self.client.get(reverse('executive:category'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_accept_order(self):
        response = self.client.get(reverse('executive:create_product'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_cancle_order(self):
        response = self.client.get(reverse('executive:product'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_outfordelivery_order(self):
        response = self.client.get(reverse('executive:editproduct'))
        self.assertEqual(response.status_code, 302)


    def test_view_uses_correct_template_delivered_order(self):
        response = self.client.get(reverse('executive:deleteproduct'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_notificatons(self):
        response = self.client.get(reverse('executive:deletecategory'))
        self.assertEqual(response.status_code, 302)