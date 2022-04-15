from django.db import models
#from users.models import User

# Create your models here.


class CertificationCenter(models.Model):
    center_name = models.CharField(max_length=500, null=False, blank=False)
    establishment = models.CharField(max_length=500, null=False, blank=False)
    address = models.CharField(max_length=500, null=False, blank=False)
    #protectors = models.ManyToManyField(User, related_name='protectors')

    def _str_(self):
        return self.center_name
