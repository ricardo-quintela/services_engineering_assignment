import random
from django.http import HttpRequest, JsonResponse

from rest_framework.decorators import api_view

from DEV.clinic.aws_middleware.stepfunctions import execute_workflow
from DEV.clinic.clinic.settings import STATE_MACHINE_ARN

ENTIDADE = 12345

@api_view(["GET"])
def payment_option(request: HttpRequest, option: int, telemovel: int) -> JsonResponse:
    
    response = execute_workflow(
        {
            "type": "requestIdempotencyKey",
            "appointement_id": 2
        },
        STATE_MACHINE_ARN
    )
    
    if "error" in response.content.keys():
        return JsonResponse({"error": "Escolha uma opção válida."})
    
    if option == 1:
        valor: float = random.randint(5, 25)
        return JsonResponse({"telemovel": telemovel, "valor": valor})
    elif option == 2:
        referencia: int = random.randint(111111111, 999999999)
        valor: float = random.randint(5, 25)
        return JsonResponse({"entidade": ENTIDADE, "referencia": referencia, "valor": valor})
    elif option == 3:
        valor: float = random.randint(5, 25)
        return JsonResponse({"valor": valor})
    else:
        return JsonResponse({"error": "Escolha uma opção válida."})