import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from recommend.service.recommendation_engine import EmbeddingRecommender

@csrf_exempt
@login_required
def get_recommendations(request):
    req_body = json.loads(request.body)
    username = req_body["username"]
    try:
        recommender = EmbeddingRecommender(username)
        recommendations = recommender.generate_recommendations()
        return JsonResponse({"recommendations": recommendations}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)