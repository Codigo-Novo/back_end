from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpRequest, JsonResponse
import json
from .models import DonationToken
from django.contrib.auth.models import User
from cadastro.models import Institution

@api_view(['POST'])
def generateDonationToken(request: HttpRequest):
    try:
        data = request.data
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    
    id = data.get('institution')
    institution = Institution.objects.get(id=id)
    user = User.objects.get(id=institution.user.id)
    description = data.get('description')
    token = DonationToken.objects.create(created_by=user, description=description)
    return JsonResponse({"Token": token.token})

@api_view(['POST'])
def generateDonation(request: HttpRequest):
    try:
        data = request.data
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    
    id = data.get('institution')
    institution = Institution.objects.get(id=id)
    user = User.objects.get(id=institution.user.id)
    description = data.get('description')
    donatoruser = data.get('donator')
    try:
        donator = User.objects.get(username=donatoruser)
    except:
        return JsonResponse({'message': 'Usuário não encontrado ou inexistente.'}, status=400)
    token = DonationToken.objects.create(created_by=user, description=description)
    token.redeem(donator)
    return JsonResponse({"Token": token.token})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def redeemDonationToken(request: HttpRequest):
    try:
        data = request.data
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    
    token_value = data.get('token')
    token = DonationToken.objects.filter(token=token_value, is_redeemed=False).first()

    if token and token.redeem(request.user):
        return JsonResponse({
            "success": "Doação registrada com sucesso",
            "redeemed_at": token.redeemed_at,
            "redeemed_by": token.redeemed_by.username
        })
    
    return JsonResponse({"error": "Token inválido ou já resgatado"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def getDonatorDonations(request: HttpRequest):
    user = request.user
    donations = DonationToken.objects.filter(redeemed_by=user).select_related("created_by").values(
        "description", "redeemed_at", "created_by__first_name"
    )
    total_donations = donations.count()

    return JsonResponse({"user": user.username, 
                         "total_donations": total_donations, 
                         "donations": list(donations)})

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def getInstitutionDonations(request: HttpRequest):
    user = request.user
    donations = DonationToken.objects.filter(created_by=user).select_related("redeemed_by").values(
        "token", "description", "is_redeemed", "created_at", "redeemed_at", "redeemed_by__first_name"
    )
    total_donations = donations.count()
    redeemed_count = donations.filter(is_redeemed=True).count()

    return JsonResponse({"user": user.username, 
                         "total_donations": total_donations,
                         "redeemed_donations": redeemed_count, 
                         "donations": list(donations)})