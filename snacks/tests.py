from django.test import TestCase
from django.urls import reverse
from .models import Snack
from django.contrib.auth import get_user_model


class SnacksTest(TestCase):
    def test_home_page_status_code(self):
        url = reverse('snack_list')
        print(f"The url is {url}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def setUp(self):
        reviewer = get_user_model().objects.create(username="tester1",password="tester")
        Snack.objects.create(name="rake", reviewer=reviewer)
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

    def test_list_page_status_code(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_page_template(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertTemplateUsed(response, 'base.html')


    def test_detail_page_status_code(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_template(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_detail_page_context(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        snack = response.context['snack']
        self.assertEqual(snack.name, "rake")
        self.assertEqual(snack.reviewer.username, "tester1")

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"name": "Updated name", "rating": 3, "reviewer": self.user.id, "description": "test description",
             "image_url": "testimageurl.com", "reference_url": "testreferenceurl.com"}
        )

        self.assertRedirects(response, reverse("snack_list"), target_status_code=200)

    def test_thing_update_bad_url(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"name": "Updated name", "rating": 3, "reviewer": self.user.id, "description": "test description",
             "image_url": "badurl", "reference_url": "testreferenceurl.com"}
        )

        self.assertEqual(response.status_code, 200)


    def test_model(self):
        snack = Snack.objects.create(name="rake", reviewer=self.user)
        self.assertEqual(snack.name, "rake")
