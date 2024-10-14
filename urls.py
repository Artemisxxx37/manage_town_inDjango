from django.urls import path
from . import views

urlpatterns = [
	path('' ,views.home, name = "home"),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login_views, name='login'),
	path('dashboard/', views.dashboard_view, name= 'dashboard'),
	path('logout/', views.logout_view ,name='logout'),
	path('administration/', views.restricted_view, name="administration"),
	path('administrator/',views.site_admin, name="administrator"),
	path('add_building/', views.add_building, name='add_building'),
	path('building/<pk>/edit/', views.edit_building, name='building_edit'),
	path('building/<pk>/delete/', views.delete_building, name='building_delete'),
	path('create_intervention/', views.create_intervention, name='create_intervention'),
	path('interventions/', views.intervention_list_view, name='intervention_list'),
	path('interventions/<pk>/delete/', views.delete_intervention, name='delete_intervention'),
	path('interventions/<pk>/mark_as_done/', views.mark_as_done, name='mark_as_done'),
	path('report/', views.report_incident, name='report_incident'),
	path('report/success/', views.incident_report_success, name='incident_report_success'),
	path('incidents/', views.list_incidents, name='list_incidents'),

]