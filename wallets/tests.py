from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Wallet


# Create your tests here.
class WalletTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )

        cls.wallet = Wallet.objects.create(
            author=cls.user,
            balance=10000,
        )

    def test_wallet_model_content(self):
        self.assertEqual(self.wallet.author.username, "testuser")
        self.assertEqual(self.wallet.balance, 10000)

    def test_wallet_api_listview(self):
        response = self.client.get(reverse("wallet_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertContains(response, self.wallet.balance)

    def test_wallet_api_detailview(self):
        response = self.client.get(
            reverse("wallet_detail", kwargs={"pk": self.wallet.id}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertContains(response, 10000)


class WalletOperationTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )
        self.wallet = Wallet.objects.create(
            author=self.user,
            balance=1000,
        )

    def test_deposit_success(self):
        url = reverse("wallet_operation", args=[self.wallet.id])
        data = {"operationType": "DEPOSIT", "amount": 500}
        response = self.client.post(url, data, format="json")
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.wallet.balance, 1500)

    def test_withdraw_success(self):
        url = reverse("wallet_operation", args=[self.wallet.id])
        data = {"operationType": "WITHDRAW", "amount": 300}
        response = self.client.post(url, data, format="json")
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.wallet.balance, 700)

    def test_withdraw_insufficient_funds(self):
        url = reverse("wallet_operation", args=[self.wallet.id])
        data = {"operationType": "WITHDRAW", "amount": 2000}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Insufficient funds.")

    def test_invalid_operation_type(self):
        url = reverse("wallet_operation", args=[self.wallet.id])
        data = {"operationType": "INVALID_OPERATION", "amount": 500}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_not_found(self):
        url = reverse("wallet_operation", args=[9999])
        data = {"operationType": "DEPOSIT", "amount": 500}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Wallet not found.")
