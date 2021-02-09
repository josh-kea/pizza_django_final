from rest_framework import permissions
from django.contrib.auth.models import User
from .models import UserProfile

class IsEmployeeOrNoAccess(permissions.BasePermission):
    """
    Global permission check if user is employee
    """

    def has_permission(self, request, view):
        print("USER TRYING TO ACCESS API!: "+ str(request.user))
        userprofile = UserProfile.objects.get(user=request.user)
        print("USER TRYING TO ACCESS API!: "+ str(userprofile.user_status))
        
        if userprofile.isEmployee:
            print(str(request.user.username) + " has permission to view " + str(view))
            return True