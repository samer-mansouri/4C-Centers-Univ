from .models import Protector, Student, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_restql.mixins import DynamicFieldsMixin
from django.contrib.auth.models import Group
from rest_framework_simplejwt.settings import api_settings


class FullProtectorSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class ProtectorSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
                
        estab = serializers.SerializerMethodField('get_estab_name')
        class Meta:
                model = Protector
                fields = ['start_date', 'end_date', 'phone_number', 'establishment', 'estab']

        def get_estab_name(self, post):
          username = post.establishment.center_name
          return username
    protector = ProtectorSerializer()
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        model = User
        extract_kwargs = {
          'password': {'write_only': True}
        }
        fields = ['id', 'email', 'username', 'first_name', 'last_name',  'password', 'password2', 'protector']
        read_only_fields = ('id',)

    def save(self):

      protector_data = self.validated_data.pop('protector')      
      user = User(
        email=self.validated_data["email"],
        username = self.validated_data["username"],
        first_name=self.validated_data["first_name"],
        last_name=self.validated_data["last_name"],        
      )

      password = self.validated_data["password"]
      password2 = self.validated_data["password2"]

      if password != password2:
        raise serializers.ValidationError({'password': 'Password Must Match'})
      if password == user.username:
        raise serializers.ValidationError({'password': 'Password must be different of username'})
      if password == user.email:
        raise serializers.ValidationError({'password': 'Password must be different of email'})
      if len(password) < 8:
        raise serializers.ValidationError({'password': 'Password length must be over 8 charachters'})
      
      
      user.set_password(password)
      user.is_protector = True
      #protectors = Group.objects.get(name='Protectors') 
      #user.groups.add(protectors)
      user.save()
      Protector.objects.create(protector=user, **protector_data)
      return user

    def update(self):
      instance = self.instance
      validated_data = self.validated_data
      protector_data = validated_data.pop('protector')
      protector = instance.protector
      instance.first_name = validated_data.get('first_name', instance.first_name)
      instance.last_name = validated_data.get('last_name', instance.last_name)
      instance.username = validated_data.get('username', instance.username)
      instance.email = validated_data.get('email', instance.email)
      instance.save()

      protector.start_date = protector_data.get('start_date', protector.start_date)
      protector.end_date = protector_data.get('end_date', protector.end_date)
      protector.phone_number = protector_data.get('phone_number', protector.phone_number)
      protector.establishment = protector_data.get('establishment', protector.establishment)
      protector.save()
      return instance
    
    def to_representation(self, obj):
        rep = super(FullProtectorSerializer, self).to_representation(obj)
        rep.pop('password', None)
        return rep

class ProtectorUpdateSerializer(serializers.ModelSerializer):

  class ProtectorUSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
                
        
        class Meta:
                model = Protector
                fields = ['start_date', 'end_date', 'phone_number', 'establishment']
                
    
  protector = ProtectorUSerializer()

  class Meta:
      model = User
      fields = ['email', 'username', 'first_name', 'last_name',  'password', 'protector']


class FullStudentSerializer(serializers.ModelSerializer):

    class StudentSerializer(serializers.ModelSerializer):
                
        
        class Meta:
                model = Student
                fields = ['establishment', 'diploma', 'level_of_studies', 'phone_number']

    student = StudentSerializer()
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',  'password', 'password2', 'student']
        read_only_fields = ('id', )
        extract_kwargs = {
          'password': {'write_only': True}
        }
    
    def save(self):

      student_data = self.validated_data.pop('student')      
      user = User(
        email=self.validated_data["email"],
        username = self.validated_data["username"],
        first_name=self.validated_data["first_name"],
        last_name=self.validated_data["last_name"],        
      )
      password = self.validated_data["password"]
      password2 = self.validated_data["password2"]

      if password != password2:
        raise serializers.ValidationError({'password': 'Password Must Match'})
      if password == user.username:
        raise serializers.ValidationError({'password': 'Password must be different of username'})
      if password == user.email:
        raise serializers.ValidationError({'password': 'Password must be different of email'})
      if len(password) < 8:
        raise serializers.ValidationError({'password': 'Password length must be over 8 charachters'})
      
      
      user.set_password(password)
      user.is_student = True
      user.save()
      Student.objects.create(student=user, **student_data)
      return user

    
    def to_representation(self, obj):
        rep = super(FullStudentSerializer, self).to_representation(obj)
        rep.pop('password', None)
        return rep


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        #token['name'] = user.first_name + " " + user.last_name
        if user.is_protector and not user.is_student:
            token['role'] = 'protector'
        elif user.is_student and not user.is_protector:
            token['role'] = 'student'
        elif not user.is_protector and not user.is_student:
            token['role'] = 'admin'

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['name'] = self.user.first_name + " " + self.user.last_name
        if self.user.is_protector and not self.user.is_student:
            data['role'] = 'protector'
        elif self.user.is_student and not self.user.is_protector:
            data['role'] = 'student'
        elif not self.user.is_protector and not self.user.is_student:
            data['role'] = 'admin'

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


