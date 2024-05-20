import random
import time
from django.http import HttpRequest, JsonResponse

from rest_framework.decorators import api_view
from authentication.jwt import perm_required

import json
import boto3

ENTIDADE = 12345

@api_view(["GET"])
def payment_option(request: HttpRequest, option: int) -> JsonResponse:
    
    if option == 1:
        referencia: int = random.randint(111111111, 999999999)
        valor: float = random.randint(5, 25)
        return JsonResponse({"entidade": ENTIDADE, "referencia": referencia, "valor": valor})
    elif not option:
        telemovel = request.data.get("telemovel")
        return JsonResponse({"telemovel": telemovel, "valor": valor})
    else:
        return JsonResponse({"error": "choose a valid option!"})
