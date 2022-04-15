from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import CertificationCenterSerializer
from .models import CertificationCenter
from rest_framework import viewsets


class CertificationCenterView(viewsets.ModelViewSet):
    queryset = CertificationCenter.objects.all()
    serializer_class = CertificationCenterSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAdminUser]
