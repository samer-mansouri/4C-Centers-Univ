from rest_framework import serializers

from .models import CertificationSession, RegisterInSession


class CertificationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationSession
        fields = '__all__'

class StudentGetCertificationSessionSerializer(serializers.ModelSerializer):
    
    is_participated = serializers.SerializerMethodField('participated')

    def participated(self, obj):
        request = self.context.get("request")
        user = request.user
        print(user)
        try:
            RegisterInSession.objects.get(session=obj.id, student=user)
            return True
        except RegisterInSession.DoesNotExist:
            return False
        
    class Meta:
        model = CertificationSession
        fields = '__all__'

    



class RegisterInSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisterInSession
        fields = '__all__'