from django.db import models

# Create your models here.

class Projects(models.Model):
    ProjectID=models.CharField(max_length=10)
    Name=models.CharField(max_length=30)
    Description=models.CharField(max_length=200)
    Image=models.CharField(max_length=30) 
    Admin=models.CharField(max_length=30)
    Member=models.CharField(max_length=200)

class DockerFiles(models.Model):
    Name=models.CharField(max_length=30)
    Size=models.CharField(max_length=30)
    Created=models.CharField(max_length=100)
    CreatedBy=models.CharField(max_length=30)
    Modified=models.CharField(max_length=100)
    ModifiedBy=models.CharField(max_length=30)
    Path=models.CharField(max_length=300)
