import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Building , Intervention
from .models import Incident

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'style': 'color: #00698f;'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'style': 'color: #00698f;'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        help_texts = {

            'username': '',  # Set help_text to an empty string

        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email

    
 

    def clean_password(self):
        """Check that the password meets complexity requirements."""
        password = self.cleaned_data['password']
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')

        if not re.search(r"[A-Z]", password):
            errors.append('Password must contain at least one uppercase letter.')

        if not re.search(r"[a-z]", password):
            errors.append('Password must contain at least one lowercase letter.')

        if not re.search(r"\d", password):
            errors.append('Password must contain at least one digit.')

        if not re.search(r"[!@#$%^&*()_+=-{};:'<>,./?]", password):
            errors.append('Password must contain at least one special character.')

        if errors:
            self.add_error('password', '\n'.join(errors))
        return password



    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Passwords do not match')
        return confirm_password


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'style': 'color: #00698f;'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise ValidationError('Username does not exist')
        return username

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise ValidationError('Password is incorrect')
        return password


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'address', 'description', 'health_status', 'health_status_color')

    health_status = forms.IntegerField(label='Health Status (%)')
    health_status_color = forms.CharField(label='Health Status Color', max_length=10)

    def save(self, commit=True):
        building = super().save(commit=False)
        building.health_status = self.cleaned_data['health_status']
        building.health_status_color = self.cleaned_data['health_status_color']
        if commit:
            building.save()
        return building

class InterventionForm(forms.ModelForm):

    class Meta:

        model = Intervention

        fields = ('intervention_type', 'intervention_date', 'intervention_notes')



class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ('title', 'description', 'date_occurred', 'location')