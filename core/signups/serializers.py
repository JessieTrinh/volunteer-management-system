# File: signups/serializers.py
# Purpose:
#   Converts model instances into plain JSON for the API.
#   Keeping these serializers simple helps the front end stay clean
#   because the browser only gets the fields it actually needs.

from rest_framework import serializers

from .models import (
    Volunteer,
    Coordinator,
    Role,
    Enrollment,
    Certificate,
    CulturalInterest,
    Post,   # added for announcement posts
    VolunteerWorkPhoto,   # added for work photo gallery
)

# -------------------------------------------------------------
# Simple serializer for cultural interest tags
# -------------------------------------------------------------
class CulturalInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalInterest
        fields = "__all__"


# -------------------------------------------------------------
# Certificates used by volunteers
# -------------------------------------------------------------
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"


# -------------------------------------------------------------
# Basic volunteer information
# -------------------------------------------------------------
class VolunteerSerializer(serializers.ModelSerializer):
    cultural_interests = CulturalInterestSerializer(many=True, read_only=True)
    
    class Meta:
        model = Volunteer
        fields = "__all__"
    
    def update(self, instance, validated_data):
        cultural_interests_data = self.initial_data.get('cultural_interests', [])
        
        # Update other fields normally
        for attr, value in validated_data.items():
            if attr != 'cultural_interests':
                setattr(instance, attr, value)
        
        # Handle cultural_interests separately
        if cultural_interests_data is not None:
            # Clear existing cultural interests
            instance.cultural_interests.clear()
            # Add new cultural interests
            for interest_id in cultural_interests_data:
                try:
                    interest = CulturalInterest.objects.get(id=interest_id)
                    instance.cultural_interests.add(interest)
                except CulturalInterest.DoesNotExist:
                    pass  # Skip invalid interest IDs
        
        instance.save()
        return instance


# -------------------------------------------------------------
# Coordinator information for community organizations
# -------------------------------------------------------------
class CoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinator
        fields = "__all__"


# -------------------------------------------------------------
# Roles include cultural themes for EmiExplorer later
# -------------------------------------------------------------
class RoleSerializer(serializers.ModelSerializer):
    cultural_themes = CulturalInterestSerializer(many=True, read_only=True)
    coordinator = CoordinatorSerializer(read_only=True)
    language_level = serializers.CharField()
    task_complexity = serializers.CharField()

    class Meta:
        model = Role
        fields = "__all__"


# -------------------------------------------------------------
# Volunteer work photos for profile gallery
# -------------------------------------------------------------
class VolunteerWorkPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerWorkPhoto
        fields = "__all__"


# -------------------------------------------------------------
# Enrollments connect volunteers and roles
# -------------------------------------------------------------
class EnrollmentSerializer(serializers.ModelSerializer):
    volunteer = VolunteerSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    work_photos = VolunteerWorkPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"


# -------------------------------------------------------------
# Serializer for simple announcement posts
# -------------------------------------------------------------
class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = "__all__"
