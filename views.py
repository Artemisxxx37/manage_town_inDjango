from django.shortcuts import render, HttpResponse , redirect
from django.contrib.auth import authenticate, login
from .models import Building , BuildingHealthStatus
from django.contrib.auth.views import LogoutView
from .forms import LoginForm
from django_filters import filters
from .forms import BuildingForm , InterventionForm
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django_filters import rest_framework as filters
from .models import Intervention 


from .forms import IncidentReportForm
from .models import Incident


@login_required
def restricted_view(request):
    return render(request, 'restricted.html')

def home(request):
	return render(request, "home.html")

def signup(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            try:

                user = form.save(commit=False)

                user.set_password(form.cleaned_data['password'])

                user.save()

                return redirect('login')

            except ValidationError as e:

                return render(request, 'signup.html', {'form': form, 'error': e.message})

        else:

            if 'password' in form.errors:

                form = UserRegistrationForm()

            return render(request, 'signup.html', {'form': form})

    else:

        form = UserRegistrationForm()

        return render(request, 'signup.html', {'form': form})

def login_views(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    return render(request, "home.html")

def site_admin(request):
    return LogoutView.as_view()(request)

@login_required
def dashboard_view(request):

    buildings = Building.objects.all()

    return render(request, 'dashboard.html', {'buildings': buildings})

def add_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save()
            health_status = form.cleaned_data['health_status']
            health_status_color = form.cleaned_data['health_status_color']
            BuildingHealthStatus.objects.create(building=building, health_status=health_status, health_status_color=health_status_color)
            return redirect('dashboard')
    else:
        form = BuildingForm()
    return render(request, 'add_building.html', {'form': form})

def edit_building(request, pk):
    building = Building.objects.get(pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            health_status = form.cleaned_data['health_status']
            health_status_color = form.cleaned_data['health_status_color']
            BuildingHealthStatus.objects.filter(building=building).delete()
            BuildingHealthStatus.objects.create(building=building, health_status=health_status, health_status_color=health_status_color)
            return redirect('dashboard')
    else:
        form = BuildingForm(instance=building)
    return render(request, 'building_edit.html', {'form': form})


def delete_building(request, pk):

    building = Building.objects.get(pk=pk)

    if request.method == 'POST':

        building.delete()

        return redirect('dashboard')

    return render(request, 'building_delete.html')

def create_intervention(request):

    if request.method == 'POST':

        form = InterventionForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = InterventionForm()

    return render(request, 'intervention.html', {'form': form})

def intervention_list_view(request):

    interventions = Intervention.objects.all()

    return render(request, 'interventions.html', {'interventions': interventions})


def delete_intervention(request, pk):
    intervention = Intervention.objects.get(pk=pk)
    intervention.delete()
    return redirect(reverse_lazy('intervention_list'))

def mark_as_done(request, pk):
    intervention = Intervention.objects.get(pk=pk)
    intervention.done = True
    intervention.save()
    return redirect(reverse_lazy('intervention_list'))

@login_required

def report_incident(request):

    if request.method == 'POST':

        form = IncidentReportForm(request.POST)

        if form.is_valid():

            incident = form.save(commit=False)

            incident.reported_by = request.user

            incident.save()

            return redirect('incident_report_success')

    else:

        form = IncidentReportForm()

    return render(request, 'incident_report.html', {'form': form})
def incident_report_success(request):

    return render(request, 'dashboard.html')

def list_incidents(request):

    incidents = Incident.objects.all() 

    return render(request, 'list_incidents.html', {'incidents': incidents})