from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from payment.models import *
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Register(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    phone=PhoneNumberField()
    

    customer='customer'
    staff='staff'

    user_types=[
        (customer,'customer'),
        (staff,'staff')
    ]
    user_type=models.CharField(max_length=30,choices=user_types,default=customer)

    def __str__(self):
        return str(self.user.username)



class Complaints(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateTimeField(default=timezone.now)
    content=models.TextField()
    reason=models.TextField()
    def __str__(self):
        return str(self.content)


class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    content=models.TextField()
    def __str__(self):
        return str(self.content)


class Requiremt(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    staff=models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    description=models.TextField()
    square_feet=models.IntegerField()
    date=models.DateTimeField(default=timezone.now)
    finished='finished'
    notfinished='notfinished'
    statuses=[
        (finished,'finished'),
        (notfinished,'notfinished')
    ]
    status=models.CharField(max_length=30,choices=statuses,default=notfinished)
    demo=models.FileField(upload_to='files',null=True,blank=True)
    message=models.CharField(max_length=100,null=True,blank=True)
    paid=models.BooleanField(default=False)
    work=models.FileField(upload_to='files',null=True,blank=True)
    ten='10%'
    twenty='20%'
    thirty='30%'
    fourty='40%'
    fifty='50%'
    sixty='60%'
    seventy='70%'
    eighty='80%'
    ninety='90%'
    hundred='100%'
    percentages=[
        (ten,'10%'),
        (twenty,'20%'),
        (thirty,'30%'),
        (fourty,'40%'),
        (fifty,'50%'),
        (sixty,'60%'),
        (seventy,'70%'),
        (eighty,'80%'),
        (ninety,'90%'),
        (hundred,'100%')

    ]

    percentage=models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return str(self.description)


class Chat(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    staff=models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    content=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.content)


class Leave(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    startdate=models.DateField(null=True,blank=True)
    days=models.IntegerField()
    SICK = 'sick'
    CASUAL = 'casual'
    EMERGENCY = 'emergency'
    STUDY = 'study'

    LEAVE_TYPE = [
        (SICK,'Sick Leave'),
        (CASUAL,'Casual Leave'),
        (EMERGENCY,'Emergency Leave'),
        (STUDY,'Study Leave'),
    ]

    reason=models.CharField(max_length=50,choices=LEAVE_TYPE,default=SICK)
    approved='approved'
    pending='pending'
    reject="reject"
    statuses=[
        (approved,'approved'),
        (pending,'pending'),
        (reject,'reject')
    ]
    status=models.CharField(max_length=30,choices=statuses,default=pending)
    date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.user)



class PriceTable(models.Model):
    base=models.IntegerField()
    upper=models.IntegerField()
    price=models.IntegerField()
    def __str__(self):
        return str(self.price)




