from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

@ensure_csrf_cookie
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})