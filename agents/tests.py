
# Create your tests here.
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



    def test_view_uses_correct_template_AgentDetailsView(self):
        response = self.client.get(reverse('agent:home'))
        self.assertEqual(response.status_code, 302)


    def test_view_uses_correct_template_viewprofile(self):
        response = self.client.get(reverse('agent:viewprofile'))
        self.assertEqual(response.status_code, 302)
        
    def test_view_uses_correct_template_all_orders(self):
        response = self.client.get(reverse('agent:all_orders'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_order(self):
        response = self.client.get(reverse('agent:order'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_incomingorders(self):
        response = self.client.get(reverse('agent:incomingorders'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_assignedorders(self):
        response = self.client.get(reverse('agent:assignedorders'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_completedorders(self):
        response = self.client.get(reverse('agent:completedorders'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_cancledorders(self):
        response = self.client.get(reverse('agent:cancledorders'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_accept_order(self):
        response = self.client.get(reverse('agent:accept_order'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_cancle_order(self):
        response = self.client.get(reverse('agent:cancle_order'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_outfordelivery_order(self):
        response = self.client.get(reverse('agent:outfordelivery_order'))
        self.assertEqual(response.status_code, 302)


    def test_view_uses_correct_template_delivered_order(self):
        response = self.client.get(reverse('agent:delivered_order'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template_notificatons(self):
        response = self.client.get(reverse('agent:notificatons'))
        self.assertEqual(response.status_code, 302)

