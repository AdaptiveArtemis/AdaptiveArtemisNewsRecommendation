import json
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from rest_framework.settings import api_settings

from news.models import Article
from .models import User, NewsLog

# Create your views here.

# Parse the json file sent by the react frontend and register it
# 注册和登录是不需要@login_required

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            email = data['email']
            password = data['password']

            if not username or not email or not password:
                return JsonResponse({'message': 'Invalid request body'}, status=400)
            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'User already exists'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already exists'}, status=400)
            # Create the user and save it to the database
            user = User(
                username=username,
                email=email,
                preferList={}
            )
            user.set_password(password)
            user.save()

            # Returns the successful registration information
            return JsonResponse({'message': 'User registered successfully'}, status=200)
        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


# login
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # usename = data.get('usename')
            email = data.get('email', None)
            password = data.get('password')

            user = User.objects.filter(email=email).first()

            if user:
                if user.is_first_login:
                    return JsonResponse({
                        'message': 'Login successful',
                        'is_First_Login': True,
                        'username': user.username,
                    }, status=200)
                else:
                    return JsonResponse({
                        'message': 'Login successful',
                        'is_First_Login': False,
                        'username': user.username,
                    }, status=200)
            else:
                return JsonResponse({'message': 'User does not exist'}, status=400)
            # user = authenticate(usename=usename, password=password)
            # user = authenticate(email=email, password=password)

            # if user is not None:
            #     login(request, user)
            #     if user.is_first_login:
            #         return JsonResponse({
            #             'message': 'Login successful',
            #             'is_First_Login': True,
            #             'username': user.username,
            #         }, status=200)
            #     else:
            #         return JsonResponse({
            #             'message': 'Login successful',
            #             'is_First_Login': False,
            #             'username': user.username,
            #         }, status=200)
            # else:
            #     return JsonResponse({'message': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid request body'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


def normalize_prefer_list(prefer_list):
    # Normalize the prefer list to a list of strings,prefer_list is a dictionary
    total_weight = sum(prefer_list.values())

    if total_weight:
        normalized_prefer_list = {keyword: weight / total_weight for keyword, weight in prefer_list.items()}
    else:
        normalized_prefer_list = {keyword: 0 for keyword in prefer_list.keys()}

    return normalized_prefer_list


@csrf_exempt
# @login_required
def get_user_profile(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        current_user = User.objects.filter(username=username).first()
        try:
            prefer_list = current_user.preferList
            if not prefer_list:
                normalized_prefer_list = "No preferences set"
            else:
                normalized_prefer_list = normalize_prefer_list(prefer_list)

            recent_news_logs_query = (NewsLog.objects.filter(user=current_user)      # front-end
                                .order_by('-timestamp')[:10])

            if not recent_news_logs_query:
                recent_news_logs = "No recent news logs found"
            else:
                recent_news_logs = [
                    {
                        'title': log.title,
                        'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for log in recent_news_logs_query
                ]

            user_info = {
                'username': current_user.username,
                'email': current_user.email,
                'preferList': normalized_prefer_list,
                'recentNewsLogs': list(recent_news_logs)
            }
            return JsonResponse(user_info, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
# @login_required
@require_http_methods(['POST'])
def update_prefer_list(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        current_user = User.objects.filter(username=username).first()
        categories = data.get('prefer_list')
        is_first_login = data.get('is_first_login', True)
        if isinstance(categories, list) and len(categories) == 5:
            prefer_list = {category: 7 for category in categories}
            current_user.set_prefer_list(prefer_list)

            if not is_first_login:
                current_user.is_first_login = False

            current_user.save()
            return JsonResponse({'message': 'Preference list updated successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid request body'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid request body'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@csrf_exempt
# @login_required
def log_news(request):
    # user: User = request.user
    # news_id = request.POST.get('news_id')
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        user = User.objects.filter(username=username).first()
        title = data.get('title')

        try:
            article = Article.objects.get(title=title)
            NewsLog.objects.create(
                user=user, # user_id=user.id
                news_id=article.id,
                body=article.body,
                keywords1=article.keywords1,
                timestamp=timezone.now(),
                title=article.title
            )

            return JsonResponse({'message': 'News logged successfully'}, status=200)
        except Article.DoesNotExist:
            return JsonResponse({'message': 'News not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


