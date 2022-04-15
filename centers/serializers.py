from rest_framework import serializers

from .models import CertificationCenter


class CertificationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationCenter
        fields = '__all__'

