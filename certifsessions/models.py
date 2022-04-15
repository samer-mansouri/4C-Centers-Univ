from django.db import models
from users.models import User

# Create your models here.


class CertificationSession(models.Model):
    TYPE = [
        ('VIRTUAL', 'Virtual'),
        ('FACETOFACE', 'Face To Face')
    ]
    session_name = models.CharField(max_length=500, null=False, blank=False)
    session_date = models.DateField()
    duration = models.DurationField()
    start_time = models.TimeField()
    expire_date = models.DateField()
    number_machines = models.IntegerField()
    type = models.CharField(max_length=200, choices=TYPE)
    class_number = models.IntegerField(null=True)
    meet_link = models.CharField(max_length=500, blank=True)
    avatar = models.ImageField(
        default="formation.jpg", blank=True, null=True, upload_to='sessions')
    protector = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, blank=True, related_name='participants')


    def _str_(self):
        return self.session_name

class RegisterInSession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(CertificationSession, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

