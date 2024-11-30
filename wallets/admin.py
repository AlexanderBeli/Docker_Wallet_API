from django.contrib import admin

from .models import Wallet


# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "balance",
    )


admin.site.register(Wallet)
