import json
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import cv2

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
        
class TempFileTest(models.Model):
    img = models.ImageField(upload_to='mediaimage/')

class Division(models.Model):
    div_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.div_name

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'students/{}/{}/{}/{}'.format(instance.dept, instance.div,instance.usn, filename)

def model_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'models/{}/{}/{}'.format(instance.dept, instance.div, filename)

class ModelTrained(models.Model):
    model = models.FileField(upload_to=model_directory_path)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    div = models.ForeignKey(Division, on_delete=models.CASCADE)

class Classrooms(models.Model):
    cno = models.CharField(max_length=3)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    div = models.ForeignKey(Division,on_delete=models.CASCADE)
    cip = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{str(self.cno)} - {self.dept} , {self.div}"

class Student(models.Model):
    name = models.CharField(max_length=255)
    usn = models.CharField(max_length=255)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    div = models.ForeignKey(Division,on_delete=models.CASCADE)
    img1 = models.ImageField(upload_to=user_directory_path)
    img2 = models.ImageField(upload_to=user_directory_path)
    img3 = models.ImageField(upload_to=user_directory_path)
    img4 = models.ImageField(upload_to=user_directory_path)
    img5 = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.usn
    
'''@receiver(post_save, sender=Student)
def trainModelFunc(sender, instance, **kwargs):
    from . tasks import trainModel
    st = str(instance.img1.path)
    st = r'{}'.format(st)
    newSt = os.path.split(st)
    train_dir = newSt[0]

    model_dir = os.path.split(train_dir)[0]
    for i in range(4):
        newSt = os.path.split(newSt[0])

    model_path = f"{newSt[0]}\\models\\{instance.dept}\\{instance.div}"
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    trainModel.delay(train_dir, instance.usn, model_path)'''

@receiver(post_save, sender=Student)
def trainModelFunc(sender, instance, **kwargs):
    from . tasks import trainModel
    st = str(instance.img1.path)
    st = r'{}'.format(st)
    newSt = os.path.split(st)
    train_dir = newSt[0]
    train_dir = os.path.split(train_dir)[0]
    for i in range(4):
        newSt = os.path.split(newSt[0])
    print(instance.dept, instance.div)
    model_path = f"{newSt[0]}\\models\\{instance.dept}\\{instance.div}"
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    trainModel.delay(train_dir, model_path)
