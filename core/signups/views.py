# File: signups/views.py
# Purpose:
#   Handles all HTML pages and all API viewsets.
#   View names match the URL patterns exactly to avoid errors.

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json

from .models import (
    Volunteer,
    Coordinator,
    Role,
    Enrollment,
    Certificate,
    CulturalInterest,
    Post,
    VolunteerWorkPhoto,
)

from .serializers import (
    VolunteerSerializer,
    CoordinatorSerializer,
    RoleSerializer,
    EnrollmentSerializer,
    CertificateSerializer,
    CulturalInterestSerializer,
    PostSerializer,
    VolunteerWorkPhotoSerializer,
)


# -----------------------------------------------------
# HTML PAGES
# -----------------------------------------------------

# Landing page with choice between volunteer and coordinator signup
def landing_page(request):
    return render(request, "signups/landingPage.html")

# Unified authentication page with email check
def unified_auth_page(request):
    return render(request, "signups/unified_auth.html")

# Landing page for signup/signin
def signup_landing_page(request):
    # Show signup/signin page first
    return render(request, "signups/volunteerSignup.html")

# Coordinator signup page
def coordinator_signup_page(request):
    return render(request, "signups/coordinatorSignup.html")

# Student volunteer signup page  
def volunteer_signup_page(request):
    return render(request, "signups/volunteerSignup.html")

def home_page(request):
    return render(request, "signups/home.html")


# Volunteer list page
def volunteer_list_page(request):
    return render(request, "signups/volunteer_list.html")


# Certificate upload page
def certificate_upload_page(request):
    return render(request, "signups/certificateUpload.html")


# EmiExplorer preferences page
def emi_preferences_page(request):
    return render(request, "signups/preferences.html")


# Posts list page
def posts_list_page(request):
    return render(request, "signups/posts_list.html")


# Create post page
# This was corrected to match the URL pattern
def create_post_page(request):
    return render(request, "signups/create_post.html")


# Edit post page
def edit_post_page(request):
    return render(request, "signups/edit_post.html")


# Coordinator dashboard page
def coordinator_dashboard_page(request):
    return render(request, "signups/coordinator_dashboard.html")

# Role creation page
def role_create_page(request):
    return render(request, "signups/role_create.html")

# Browse opportunities page (for volunteers)
def browse_opportunities_page(request):
    return render(request, "signups/browse_opportunities.html")

# Volunteer profile page
def volunteer_profile_page(request, volunteer_id):
    try:
        # Get volunteer data to pass to template
        volunteer = Volunteer.objects.get(id=volunteer_id)
        context = {
            'volunteer_id': volunteer_id,
            'volunteer': volunteer
        }
        return render(request, "signups/volunteer_profile_new.html", context)
    except Volunteer.DoesNotExist:
        return HttpResponse(f"Volunteer with ID {volunteer_id} not found.")
    except Exception as e:
        return HttpResponse(f"Error loading volunteer profile: {str(e)}")

# Volunteer photo upload page
def volunteer_photo_upload_page(request):
    return render(request, "signups/volunteer_photo_upload.html")

# Edit profile page (for volunteers)
def edit_profile_page(request):
    return render(request, "signups/edit_profile.html")


# Global email check function (API endpoint)
@csrf_exempt
def check_user_email(request):
    """Check if an email exists in either volunteers or coordinators"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        # Check if email exists in volunteers
        volunteer = Volunteer.objects.filter(email=email).first()
        if volunteer:
            needs_reset = volunteer.password == 'temporary_password'
            return JsonResponse({
                'exists': True,
                'user_type': 'volunteer',
                'user_id': volunteer.id,
                'name': volunteer.name,
                'needs_password_reset': needs_reset,
                'signin_url': '/volunteer-signin/',
                'dashboard_url': '/home/'
            })
        
        # Check if email exists in coordinators
        coordinator = Coordinator.objects.filter(email=email).first()
        if coordinator:
            needs_reset = coordinator.password == 'temporary_password'
            return JsonResponse({
                'exists': True,
                'user_type': 'coordinator', 
                'user_id': coordinator.id,
                'name': coordinator.name,
                'needs_password_reset': needs_reset,
                'signin_url': '/coordinator-signin/',
                'dashboard_url': '/coordinator-dashboard/'
            })
        
        # Email doesn't exist in either table
        return JsonResponse({'exists': False})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# -----------------------------------------------------
# API VIEWSETS
# -----------------------------------------------------

class CoordinatorViewSet(viewsets.ModelViewSet):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer

    def create(self, request, *args, **kwargs):
        """Create a new coordinator with hashed password"""
        data = request.data.copy()
        
        # Hash the password before saving
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        """Update coordinator with password hashing if password is being changed"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        
        # Hash the password if it's being updated
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests with password hashing"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def check_email(self, request):
        """Check if a coordinator email already exists"""
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        exists = Coordinator.objects.filter(email=email).exists()
        if exists:
            coordinator = Coordinator.objects.get(email=email)
            return Response({
                'exists': True, 
                'user_type': 'coordinator',
                'coordinator_id': coordinator.id,
                'name': coordinator.name
            })
        else:
            return Response({'exists': False})

    @action(detail=False, methods=["post"])
    def signin(self, request):
        """Sign in an existing coordinator by email and password"""
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        if not password:
            return Response({'error': 'Password is required'}, status=400)
        
        try:
            coordinator = Coordinator.objects.get(email=email)
            
            # Check if user has temporary password
            if coordinator.password == 'temporary_password':
                return Response({
                    'error': 'temporary_password',
                    'message': 'Please set up a new password for your account',
                    'needs_password_reset': True
                }, status=401)
            
            # Verify password
            if check_password(password, coordinator.password):
                return Response({
                    'success': True,
                    'coordinator_id': coordinator.id,
                    'name': coordinator.name,
                    'redirect_url': '/coordinator-dashboard/'
                })
            else:
                return Response({'error': 'Invalid password'}, status=401)
                
        except Coordinator.DoesNotExist:
            return Response({'error': 'Account not found. Please sign up first.'}, status=404)


class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

    def create(self, request, *args, **kwargs):
        """Create a new volunteer with hashed password"""
        data = request.data.copy()
        
        # Hash the password before saving
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        """Update volunteer with password hashing if password is being changed"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        
        # Hash the password if it's being updated
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests with password hashing"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def check_email(self, request):
        """Check if a volunteer email already exists"""
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        exists = Volunteer.objects.filter(email=email).exists()
        if exists:
            volunteer = Volunteer.objects.get(email=email)
            return Response({
                'exists': True, 
                'user_type': 'volunteer',
                'volunteer_id': volunteer.id,
                'name': volunteer.name
            })
        else:
            return Response({'exists': False})

    @action(detail=False, methods=["post"])
    def signin(self, request):
        """Sign in an existing volunteer by email and password"""
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        if not password:
            return Response({'error': 'Password is required'}, status=400)
        
        try:
            volunteer = Volunteer.objects.get(email=email)
            
            # Check if user has temporary password
            if volunteer.password == 'temporary_password':
                return Response({
                    'error': 'temporary_password',
                    'message': 'Please set up a new password for your account',
                    'needs_password_reset': True
                }, status=401)
            
            # Verify password
            if check_password(password, volunteer.password):
                return Response({
                    'success': True,
                    'volunteer_id': volunteer.id,
                    'name': volunteer.name,
                    'redirect_url': '/home/'
                })
            else:
                return Response({'error': 'Invalid password'}, status=401)
                
        except Volunteer.DoesNotExist:
            return Response({'error': 'Account not found. Please sign up first.'}, status=404)

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        volunteer = self.get_object()

        enrollments = Enrollment.objects.filter(volunteer=volunteer)
        certificates = Certificate.objects.filter(user=volunteer)

        data = {
            "volunteer": VolunteerSerializer(volunteer).data,
            "enrollments": EnrollmentSerializer(enrollments, many=True).data,
            "certificates": CertificateSerializer(certificates, many=True).data,
        }
        return Response(data)


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer

    def get_queryset(self):
        queryset = Role.objects.all()
        language_level = self.request.query_params.get('language_level')
        task_complexity = self.request.query_params.get('task_complexity')
        if language_level:
            queryset = queryset.filter(language_level=language_level)
        if task_complexity:
            queryset = queryset.filter(task_complexity=task_complexity)
        return queryset


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        volunteer_id = request.data.get('volunteer')
        role_id = request.data.get('role')
        if volunteer_id and role_id:
            enrollment = Enrollment.objects.create(
                volunteer_id=volunteer_id,
                role_id=role_id,
                hours_worked=request.data.get('hours_worked', 0)
            )
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data)
        return Response({'error': 'volunteer and role IDs required'}, status=400)


class CulturalInterestViewSet(viewsets.ModelViewSet):
    queryset = CulturalInterest.objects.all()
    serializer_class = CulturalInterestSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]


class VolunteerWorkPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerWorkPhotoSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        queryset = VolunteerWorkPhoto.objects.all()
        volunteer_id = self.request.query_params.get('volunteer')
        if volunteer_id:
            # Filter photos by volunteer through enrollment relationship
            queryset = queryset.filter(enrollment__volunteer_id=volunteer_id)
        return queryset.order_by('-uploaded_at')
