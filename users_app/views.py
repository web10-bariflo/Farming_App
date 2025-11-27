from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UserListAPI(APIView):
#-----------------------------------------------------------------
#         GET method (all users or specific user by uid)
#-----------------------------------------------------------------

    def get(self, request, uid=None):
        # If UID is provided → return single user
        if uid:
            try:
                user = User.objects.get(uid=uid)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If UID not provided → return all users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#-----------------------------------------------------------------
#                           POST method
#-----------------------------------------------------------------

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()   # Create user
            return Response(
                {
                    "message": "User created successfully",
                    "user": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        # If validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        