from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import OperationSerializer, WalletSerializer


class WalletList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletOperation(APIView):

    def post(self, request, WALLET_UUID):
        try:
            wallet = Wallet.objects.get(id=WALLET_UUID)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            operation_type = serializer.validated_data["operationType"]
            amount = serializer.validated_data["amount"]

            with transaction.atomic():
                wallet.refresh_from_db()

                if operation_type == "DEPOSIT":
                    wallet.balance += amount
                elif operation_type == "WITHDRAW":
                    if wallet.balance < amount:
                        return Response(
                            {"error": "Insufficient funds."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    wallet.balance -= amount

                wallet.save()
                return Response(
                    {"balance": str(wallet.balance)}, status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
