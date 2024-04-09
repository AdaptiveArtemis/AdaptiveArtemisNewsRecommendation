import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import User, NewsLog

# Create your views here.

# Parse the json file sent by the react frontend and register it
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            email = data['email']
            password = data['password']
            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'User already exists'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already exists'}, status=400)
            # Create the user and save it to the database
            user = User(
                username=username,
                email=email,
                password=make_password(password),
                preferList=[]
            )
            user.save()

            # Returns the successful registration information
            return JsonResponse({'message': 'User registered successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

# login
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_first_login:
                    return JsonResponse({
                        'message': 'Login successful',
                        'is_First_Login': True
                    }, status=200)
                else:
                    return JsonResponse({
                        'message': 'Login successful',
                        'is_First_Login': False
                    }, status=200)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid request body'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


def normalize_prefer_list(prefer_list):
    # Normalize the prefer list to a list of strings
    total_weight = sum([item['weight'] for item in prefer_list])
    for item in prefer_list:
        item['weight'] = item['weight'] / total_weight if total_weight else 0
    return prefer_list

@login_required
def get_user_profile(request):
    current_user = request.user
    if request.method == 'GET':
        try:
            prefer_list = current_user.preferList
            normalized_prefer_list = normalize_prefer_list(prefer_list)

            recent_news_logs = (NewsLog.objects.filter(user=current_user)
                                .order_by('-timestamp')[:10])
                                # .values('news_id', 'timestamp')

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

@login_required
@require_http_methods(['POST'])
def update_prefer_list(request):
    try:
        data = json.loads(request.body)
        prefer_list = data.get('prefer_list')

        if isinstance(prefer_list, list) and len(prefer_list) > 0:
            request.user.set_prefer_list(prefer_list)
            return JsonResponse({'message': 'Prefer list updated successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid prefer list'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid request body'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)