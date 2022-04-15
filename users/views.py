from .serializers import FullProtectorSerializer, FullStudentSerializer, ProtectorUpdateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken

    
class StudentRegistrationView(CreateAPIView):
  permission_classes = (AllowAny, )
  serializer_class = FullStudentSerializer

  def post(self, request, format=None):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    protector = serializer.save()
    data = {
      "Response": "User registred successfully",
      "email": protector.email,
      "username": protector.username
    }
    return Response(data)

  def get_serializer(self, *args, **kwargs):
    serializer_class = self.get_serializer_class()
    kwargs['context'] = self.get_serializer_context()
    return serializer_class(*args, **kwargs)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

##Protector CRUD
##Only Accessible For Admin
class GetProtectors(APIView):

    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication, )
    

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        queryset = User.objects.filter(is_protector=True)
        serializer = FullProtectorSerializer(queryset, many=True).data
        return Response(serializer)
  
    def post(self, request, format=None):
        serializer = FullProtectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        protector = serializer.save()
        data = {
          "Response": "Protector registred successfully",
          "email": protector.email,
          "username": protector.username
        }
        return Response(data)


  

class GetProtector(APIView):

  permission_classes = (IsAdminUser,)
  authentication_classes = (JWTAuthentication, )

  def get_object(self, pk): 
    try: 
      return User.objects.get(pk=pk) 
    except User.DoesNotExist: 
      raise Http404
  
  def get(self, request, pk, format=None):
    protector = self.get_object(pk) 
    serializer = FullProtectorSerializer(protector) 
    return Response(serializer.data) 
  
  def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({"Success":"Protector deleted successfuly"}, status=status.HTTP_200_OK)

  def put(self, request, pk):
        protector = self.get_object(pk)
        serializer = FullProtectorSerializer(protector, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.update()
            return Response({"Success": "Protector updated with success", "data" : serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetStudents(ListAPIView): 

  permission_classes = (IsAuthenticated,)
  authentication_classes = (JWTAuthentication, )
  queryset = User.objects.filter(is_student=True)
  serializer_class = FullStudentSerializer
  
   
  def check_permissions(self, request):

        if not request.user.is_protector or request.user.is_student:
                self.permission_denied(request)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"success":"logged out successfully"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
