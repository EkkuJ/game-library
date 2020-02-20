from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import OwnedSerializer
from .models import OwnedGame
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        queryset = OwnedGame.objects.all().filter(player=request.player)
        serializer_class = OwnedSerializer
        content = {'message': 'Hello, World!'}
        return Response(content)

class OwnedViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = OwnedGame.objects.all()
    serializer_class = OwnedSerializer