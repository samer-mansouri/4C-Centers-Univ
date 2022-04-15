from django.shortcuts import render

# Create your views here.
from .serializers import CertificationSessionSerializer, RegisterInSessionSerializer, StudentGetCertificationSessionSerializer
from .models import CertificationSession, RegisterInSession
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .models import CertificationSession
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from django.http import Http404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from users.serializers import FullStudentSerializer

class CertificationSessionView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )
    #parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return CertificationSession.objects.get(pk=pk)
        except CertificationSession.DoesNotExist:
            raise Http404

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = CertificationSession.objects.filter(protector=request.user).order_by('-session_date')
        #paginate_queryset = paginator.paginate_queryset(queryset, request)
        serializer = CertificationSessionSerializer(queryset, many=True).data
        data = serializer
        return Response(data)
  
    def post(self, request, format=None):
        
        p = {"protector": request.user.id}
        data = {**request.data, **p}
        #del data['avatar']
        serializer = CertificationSessionSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        
        return Response({"Success":"Certification session created with success"})

    
    def check_permissions(self, request):
        print(request.user)
        if not request.user.is_protector or request.user.is_student:
                self.permission_denied(request)

class RUDCertifcationSession(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def get_object(self, pk, user):
        try:
            return CertificationSession.objects.get(pk=pk, protector=user)
        except CertificationSession.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        session = self.get_object(pk, request.user) 
        serializer = CertificationSessionSerializer(session) 
        return Response(serializer.data) 
  
    def delete(self, request, pk):
            session = self.get_object(pk, request.user)
            session.delete()
            return Response({"Success":"Session deleted successfuly"}, status=status.HTTP_200_OK)

    def put(self, request, pk):
            session = self.get_object(pk, request.user)
            serializer = CertificationSessionSerializer(session, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Success": "Session updated with success", "data" : serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def check_permissions(self, request):
        
        if not request.user.is_protector or request.user.is_student and request.method != 'GET':
                self.permission_denied(request)

class ReadCertifcationSession(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def get_object(self, pk):
        try:
            return CertificationSession.objects.get(pk=pk)
        except CertificationSession.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        session = self.get_object(pk) 
        serializer = CertificationSessionSerializer(session) 
        return Response(serializer.data) 
  
    
    

class CertificationSessionViewForStudent(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = CertificationSession.objects.all().order_by('-session_date')
        serializer = StudentGetCertificationSessionSerializer(queryset, many=True,  context={'request': request}).data
        return Response(serializer)

    def check_permissions(self, request):

        if request.user.is_protector or not request.user.is_student:
                self.permission_denied(request)

class CertificationSessionViewForProtector(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = CertificationSession.objects.all().order_by('-session_date')
        serializer = StudentGetCertificationSessionSerializer(queryset, many=True,  context={'request': request}).data
        return Response(serializer)

    def check_permissions(self, request):

        if request.user.is_student or not request.user.is_protector:
                self.permission_denied(request)

class GetStudentSessions(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, ) 

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = CertificationSession.objects.filter(participants__pk=request.user.id).order_by('-session_date')
        paginate_queryset = paginator.paginate_queryset(queryset, request)
        serializer = StudentGetCertificationSessionSerializer(paginate_queryset, many=True,  context={'request': request}).data
        return Response(serializer)
    
    def check_permissions(self, request):

        if request.user.is_protector or not request.user.is_student:
                self.permission_denied(request)

class RetreiveSessionParticipantsForProtector(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, ) 

    def get(self, request, pk):
        try:
            queryset = CertificationSession.objects.get(pk=pk)
        except CertificationSession.DoesNotExist:
            raise Http404
        students = queryset.participants.all()
        serializer = FullStudentSerializer(students, many=True).data
        return Response(serializer)

class SessionStudentParticipationView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, ) 

    def get_object(self, pk):
        try:
            return CertificationSession.objects.get(pk=pk)
        except CertificationSession.DoesNotExist:
            raise Http404

    def get_registration_object(self, session, user):
        try:
            return RegisterInSession.objects.get(session=session, student=user)
        except RegisterInSession.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        session = self.get_object(pk) 
        if request.user in session.participants.all():
            return Response({"Warning": "User already participated"}, status=status.HTTP_302_FOUND)
        try:
            
            data = {
                "student": request.user.id,
                "session": session.id
            }
            print(data)
            serializer = RegisterInSessionSerializer(data=data)
            print(serializer)
            serializer.is_valid(raise_exception=True)
            registration = serializer.save()
            print(registration)
            session.participants.add(request.user)
            return Response({"Success":"User participated with sucess"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        session = self.get_object(pk) 
        registration = self.get_registration_object(session, request.user.id)
        try:
            session.participants.remove(request.user)
            registration.delete()
            return Response({"Success":"Registration removed with sucess"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def check_permissions(self, request):

        if request.user.is_protector or not request.user.is_student:
                self.permission_denied(request)