from django.urls import path
from .views import *

urlpatterns = [
    path('generateToken/', generateDonationToken),
    path('generateDonation/', generateDonation),
    path('redeemToken/', redeemDonationToken),
    path('getDonatorDonations/', getDonatorDonations),
    path('getInstitutionDonations/', getInstitutionDonations),
    path('editDonation/', editDonation),
    path('deleteDonation/', deleteDonation),
]