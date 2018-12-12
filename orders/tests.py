from django.test import TestCase



class UsersListViewTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     cls.client = Client()
    #     cls.user = User.objects.create_user(user_type=1, email='vhimareddy1999@gmail.com', email_verified=True)

    def test_view_url_accessible_by_name_updatedetails(self):
        self.client.login(email='vhimareddy1999@gmail.com', password='myclan#2')
        response = self.client.get(reverse('orders:order_create'))
        # self.assertTemplateUsed(response, 'home/update_details.html')
        self.assertEquals(response.status_code,200)
