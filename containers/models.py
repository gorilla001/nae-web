from django.db import models

# Create your models here.

class Containers(models.Model):

    CId = models.CharField(max_length=30)
    Name =  models.CharField(max_length=30)
    Owner =  models.CharField(max_length=30)
    PortMap = models.CharField(max_length=30)
    Created = models.CharField(max_length=30)
    Living = models.CharField(max_length=30)
    Status = models.CharField(max_length=30)
    Project = models.CharField(max_length=30)
    CodeVersion = models.CharField(max_length=30)
    
