from django.db import models
from django.utils import timezone

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pendinig'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
     ]

    complaint_id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    complaint_details = models.TextField(max_length=500,null=True,blank=True)
    complaint_location = models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default= 'Pending')
    filled_date = models.DateTimeField(default=timezone.now)

def __str__(self):
        return self.name