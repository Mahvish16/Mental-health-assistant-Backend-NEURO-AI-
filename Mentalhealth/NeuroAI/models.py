from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

response_choices=(
    ('Yes', 'Yes'),
    ('No', 'No'),
)

class RegisterUserManager(BaseUserManager):
    def create_user(self,name, email, phone_number, dob, age, address, occupation, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            dob=dob,
            age=age,
            address=address,
            occupation=occupation,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,name,email,phone_number,dob,age, address, occupation, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            dob=dob,
            age=age,
            address=address,
            occupation=occupation,
            password=password,
        )
        user.is_admin = True
        user.is_staff= True
        user.is_superuser = True
        user.save(using=self._db)
        return user 
                
class RegisterUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    dob = models.DateField()
    age = models.IntegerField()
    address = models.TextField(max_length=100)
    occupation = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects= RegisterUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ['name','phone_number','dob','age','address','occupation']
    
    def __str__(self):
        return self.name
    
class Questions (models.Model):
    question = models.CharField(max_length=100)
    
    def __str__(self):
        return self.question
    
class Disorder(models.Model):
    disorder = models.CharField(max_length=100)
    exercise = models.CharField(max_length=100)
    meditation= models.CharField(max_length=100)
    
    def __str__(self):
        return self.disorder

class DisorderSave(models.Model):
    disorder = models.ForeignKey(Disorder, on_delete= models.CASCADE)
    question = models.ForeignKey(Questions, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.question)
        
class Response(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    response = models.CharField(max_length=3,choices=response_choices)
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.response
    

    
    

    
    

    

    




