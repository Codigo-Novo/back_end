from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import secrets

class DonationToken(models.Model):
    token = models.CharField(max_length=64, unique=True, default=secrets.token_hex)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_donation_tokens")
    description = models.TextField()
    is_redeemed = models.BooleanField(default=False)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    redeemed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,  related_name="redeemed_donation_tokens")
    
    def redeem(self, user):
        if not self.is_redeemed:
            self.is_redeemed = True
            self.redeemed_at = now()
            self.redeemed_by = user
            self.save()
            return True
        return False