from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid

from core.middleware import login_exempt
from .models import User, Session, Destination
import hashlib

@login_exempt
def index(request):
    user = User.objects.all()
    session = getattr(request, 'current_session', None)
    destinations = Destination.objects.order_by('-id')[:5]
    return render(request, 'destinations/index.html', {'user': user, 'session': session, 'destinations': destinations})

def destroy_session(request):
    if request.method == 'POST':
        # Delete the Session row matching the cookie (handmade session)
        session = getattr(request, 'current_session', None)
        if session:
            session.delete()
        response = redirect('index')
        response.delete_cookie('session_token')
        return response
    return redirect('index')

@login_exempt
def create_user(request):
    return render(request, 'destinations/create_user.html')

@login_exempt
def create_session(request):
    return render(request, 'destinations/create_session.html')   

def create_destination(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = int(request.POST.get('rating'))
        share_publicly = 'share_publicly' in request.POST
        session = getattr(request, 'current_session', None)
        if not session:
            return HttpResponse("Unauthorized. You must be signed in to do this.", status=401)
        user = request.current_user
        Destination.objects.create(name=name, review=review, rating=rating, user=user, share_publicly=share_publicly)
        return redirect('index')
    return render(request, 'destinations/create_destination.html')

def users(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    name = request.POST.get('name')
    email = request.POST.get('email').strip().lower()
    password = request.POST.get('password')
    if '@' not in email or '.' not in email:
        return HttpResponse("Invalid email format", status=400)
    if User.objects.filter(email=email).exists():
        return HttpResponse("Email already in use", status=400)
    if len(password) < 8 or not any(c.isdigit() for c in password):
        return HttpResponse("Password must be 8 characters and include a number.", status=400)
    password = hashlib.sha256(password.encode()).hexdigest()
    user = User.objects.create(name=name, email=email, password_hash=password)
    token = str(uuid.uuid4())
    session = Session.objects.create(user=user, token=token)
    response = redirect('index')
    response.set_cookie('session_token', session.token, httponly=True)
    return response

def sessions(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    email = (request.POST.get('email') or '').strip().lower()
    password = (request.POST.get('password') or '')
    pw_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("Account not found", status=404)

    if user.password_hash != pw_hash:
        return HttpResponse("Incorrect password", status=401)

    session = Session.objects.create(user=user, token=str(uuid.uuid4()))
    response = redirect('index')
    response.set_cookie('session_token', session.token, httponly=True)
    return response

def destinations(request):
    session = getattr(request, 'current_session', None)
    if session:
        # Show all destinations for logged-in user
        destinations = Destination.objects.filter(user=session.user)
    else:
        # Show only publicly shared destinations for anonymous users
        return redirect('index')
    return render(request, 'destinations/destinations.html', {'destinations': destinations, 'session': session})

def edit_destination(request, destination_id):
    session = getattr(request, 'current_session', None)
    if not session:
        return HttpResponse("Unauthorized. You must be signed in to do this.", status=404)
    try:
        destination = Destination.objects.get(id=destination_id, user=session.user)
    except Destination.DoesNotExist:
        return HttpResponse("Destination does not exist or it is not your destination.", status=404)

    if request.method == 'POST':
        destination.name = request.POST.get('name')
        destination.review = request.POST.get('review')
        destination.rating = int(request.POST.get('rating'))
        destination.share_publicly = 'share_publicly' in request.POST
        destination.save()
        return redirect('destinations')

    return render(request, 'destinations/edit_destination.html', {'destination': destination})

def delete_destination(request, destination_id):
    session = getattr(request, 'current_session', None)
    if not session:
        return HttpResponse("Unauthorized. You must be signed in to do this.", status=404)
    try:
        destination = Destination.objects.get(id=destination_id, user=session.user)
    except Destination.DoesNotExist:
        return HttpResponse("Destination not found", status=404)

    if request.method == 'POST':
        destination.delete()
        return redirect('destinations')

    return HttpResponse("Method not allowed. Only POST requests are allowed.", status=404)