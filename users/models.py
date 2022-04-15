from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from centers.models import CertificationCenter
from django.conf import settings


class MyAccountManager(BaseUserManager):
  def create_user(self, email, username, password=None):
    if not email:
      raise ValueError('Users must have an email adress')
    if not username:
      raise ValueError('Users must have an username')

    user = self.model(
      email=self.normalize_email(email),
      username=username,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user  
  

  def create_superuser(self, email, username, password):
    user = self.create_user(
      email=self.normalize_email(email),
      password=password,
      username=username,
    )
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user
  
class User(AbstractBaseUser):

  email = models.EmailField(verbose_name="email", max_length=60, unique=True)
  username = models.CharField(max_length=30, unique=True)
  first_name = models.CharField(max_length=30 , unique=False)
  last_name = models.CharField(max_length=30, unique=False)
  last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  is_protector = models.BooleanField(default=False)
  is_student = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username',]

  objects = MyAccountManager()

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, app_label):
    return True

class Protector(models.Model):
    protector = models.OneToOneField(
      settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    phone_number = models.IntegerField()
    establishment = models.ForeignKey(CertificationCenter, on_delete=models.CASCADE)


    def __str__(self):
        return self.protector.username

    def delete(self, *args, **kwargs):
        user = User.objects.get(id=protector)
        user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

class Student(models.Model):
    student = models.OneToOneField(
      settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    establishment = models.CharField(max_length=55 , unique=False)
    diploma = models.CharField(max_length=55 , unique=False)
    level_of_studies = models.CharField(max_length=30 , unique=False)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.student.username