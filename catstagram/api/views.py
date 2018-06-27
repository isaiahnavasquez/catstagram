from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ProfileSerializer
from cats.models import Profile


class ProfileList(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = ProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetail(APIView):
    
    def get_object(self, username):
        try:
            return Profile.objects.filter(user__username=username).first()
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        profile = self.get_object(username)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        profile = self.get_object(username)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
