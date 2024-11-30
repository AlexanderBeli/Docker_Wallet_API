from django.urls import path

from .views import WalletList, WalletDetail, WalletOperation

urlpatterns = [
    path('<uuid:pk>/', WalletDetail.as_view(), name='wallet_detail'),
    path('<uuid:WALLET_UUID>/operation/', WalletOperation.as_view(), name='wallet_operation'),
    path('', WalletList.as_view(), name='wallet_list'),
]