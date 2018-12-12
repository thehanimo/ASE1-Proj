
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



    def test_view_uses_correct_template_customerDetailsView(self):
        response = self.client.get(reverse('customer:home'))
        self.assertEqual(response.status_code, 302)


    def test_view_uses_correct_template_viewprofile(self):
        response = self.client.get(reverse('customer:myorder'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_all_orders(self):
        response = self.client.get(reverse('customer:order'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_order(self):
        response = self.client.get(reverse('customer:order_track'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_incomingorders(self):
        response = self.client.get(reverse('customer:cancel_order'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_assignedorders(self):
        response = self.client.get(reverse('customer:editprofile'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_completedorders(self):
        response = self.client.get(reverse('customer:newprofile'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_cancledorders(self):
        response = self.client.get(reverse('customer:support'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_accept_order(self):
        response = self.client.get(reverse('customer:party_order'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_cancle_order(self):
        response = self.client.get(reverse('customer:party_orders_success'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_outfordelivery_order(self):
        response = self.client.get(reverse('customer:subscriptions'))
        self.assertEqual(response.status_code, 302)


    def test_view_uses_correct_template_delivered_order(self):
        response = self.client.get(reverse('customer:my_subscriptions'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_notificatons(self):
        response = self.client.get(reverse('customer:claim_subscription'))
        self.assertEqual(response.status_code, 302)