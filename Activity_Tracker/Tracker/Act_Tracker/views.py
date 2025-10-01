from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Activity, TimeLog

# Create your views here.
def index(request):
    activities = Activity.objects.all()
    timelogs = TimeLog.objects.all()
    return render(request, 'Tracker/index.html', {'activities': activities, 'timelogs': timelogs})

def new_activity(request):
    if request.method == 'POST':
        activity_name = request.POST.get('activity_name')
        if activity_name:
            activity = Activity.objects.create(name=activity_name)
            return redirect('activity', id=activity.id)
    return render(request, 'Tracker/new_activity.html')

def activity(request, id):
    try:
        activity = Activity.objects.get(id=id)
    except Activity.DoesNotExist:
        raise HttpResponse("<div>404: Activity does not exist</div>")
    
    # Get all time logs for this activity
    timelogs = TimeLog.objects.filter(activity=activity)
    
    return render(request, 'Tracker/activity.html', {
        'activity': activity, 
        'timelogs': timelogs
    })

def new_timelog(request, id):
    try:
        activity = Activity.objects.get(id=id)
    except Activity.DoesNotExist:
        raise HttpResponse("<div>404: Activity does not exist</div>")
    
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if start_time and end_time:
            TimeLog.objects.create(activity=activity, start_time=start_time, end_time=end_time)
            return redirect('activity', id=id)
    
    return render(request, 'Tracker/new_timelog.html', {'activity': activity})

def delete_activity(request, id):
    if request.method == 'POST':
        try:
            activity = Activity.objects.get(id=id)
            activity.delete()
            return redirect('index')
        except Activity.DoesNotExist:
            raise HttpResponse("<div>404: Activity does not exist</div>")
    return redirect('index')