from rest_framework import serializers

from .models import Wallet


# Create your views here.
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "author",
            "balance",
        )
        model = Wallet


class OperationSerializer(serializers.Serializer):
    operationType = serializers.ChoiceField(choices=["DEPOSIT", "WITHDRAW"])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
