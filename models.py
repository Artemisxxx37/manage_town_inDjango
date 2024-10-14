# models.py
from django.db import models
from django.forms.widgets import DateInput

class Building(models.Model):

    name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)

    description = models.TextField(blank=True)
    
    class Meta:
        permissions = (

                ("can_view_building", "citoyens"),

                ("can_edit_building", "permissive_uses"),

            )


    def __str__(self):

        return self.name

class BuildingHealthStatus(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    health_status = models.IntegerField()  
    health_status_color = models.CharField(max_length=10) 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.building.name} Health Status"

    



class Incident(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_occurred = models.DateField()
    location = models.CharField(max_length=255)
    reported_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Intervention(models.Model):
    intervention_type = models.CharField(max_length=255)
    intervention_date = models.DateField()
    intervention_notes = models.TextField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Intervention {self.intervention_type} on {self.intervention_date}"