from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session

# Create your models here.
'''   
class User(models.Model):
    User_Id = models.AutoField(primary_key=True)
    #User_Id = models.BigIntegerField(max_length=20,primary_key=True,auto_created=True)
    User_Name = models.CharField(max_length=30,unique=True)
    Email_Id = models.EmailField(unique=True)
    Phone_Number = models.PositiveIntegerField(max_length=10,unique=True)
    Password = models.CharField(max_length=60)
'''  

class User(AbstractUser):
    emailid = models.EmailField(unique=True)
    
      
class Security_Question(models.Model):
    Question_Id = models.AutoField(primary_key=True)
    #Question_Id = models.BigIntegerField(max_length=60,primary_key=True)
    User_Id = models.ForeignKey(User,on_delete=True,unique=True)
    Question = models.TextField(max_length=100,null=True)
    Answer = models.TextField(max_length=100,null=True)
    
class User_Details(models.Model):
    Profile_Id = models.AutoField(primary_key=True)
    #Profile_Id = models.BigIntegerField(max_length=20,primary_key=True,auto_created=True)
    User_Id = models.ForeignKey(User,on_delete=True,unique=True)
    Nick_Name = models.CharField(max_length=30,null=True)
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Not Specified', 'Not Specified'),
    )
    Gender = models.CharField(max_length=14,choices=gender,null=True,default="Male")
    Language = models.CharField(max_length=60,null=True,default="English")
    Country = models.CharField(max_length=60,null=True,default="India")
    Time_Zone = models.CharField(max_length=100,null=True,default="( GMT 5:30 ) India Standard Time(IST)")
    phone_no = models.BigIntegerField(max_length=10,null=True,default=None)
    Profile_Picture = models.FilePathField(null=True,default="/static/accounts/profile/profile.jpg")
    
class Registered_Domain(models.Model):
    Domain_Id = models.AutoField(primary_key=True)
    Domain_IP_Address = models.IPAddressField()
    Server_Name = models.CharField(max_length=30)
    Domain_Name = models.CharField(max_length=30)
    
    class Meta:
        unique_together = (('Domain_IP_Address','Server_Name','Domain_Name'))
    
class Session_Details(models.Model):
    Session_Id = models.ForeignKey(Session,on_delete=True)
    User_Id = models.ForeignKey(User,on_delete=False)
    Domain_Id = models.ForeignKey(Registered_Domain,on_delete=True)
    User_IP_Address = models.IPAddressField()
    Browser_Name = models.CharField(max_length=150)
    Login_Time = models.DateTimeField()
    Logout = models.DateTimeField(null=True)
    
    class Meta:
        unique_together = (('User_IP_Address','Browser_Name','Login_Time'),)
    
    def __unicode__(self):
        return self.User_Id.username
    
#user=User.objects.create_user(username='Saraswathy.p',first_name='shun',last_name='mathy',email='saraswathy.p@zohocorp.com',password='Shun@12')
#user.save()


