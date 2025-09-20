from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .models import Todo

# Create your views here.
def index(request):
    todos=[]
    return render(request, 'TODOS_App/index.html', {'todos': todos})

def create_todo(request):
    params = request.POST
    todo = Todo(contents=params.get('contents'))
    todo.save()
    return redirect('/')