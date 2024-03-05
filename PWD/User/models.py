from django.contrib.auth.models import BaseUserManager,UserManager,AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomerUserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email not provided")
        if not username:
            raise ValueError("Must have username")

        
        user = self.model(email=self.normalize_email(email),
                          username=username,**extra_fields)

        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,username, email, password=None, **extra_fields):
        
        #user=self.create_user(
         #   email=self.normalize_email(email), username=username,password=password
        #)
        #user.is_admin = True
        #user.is_superuser = True
        #user.save(using=self.db)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)
        
    
    
class Official(AbstractBaseUser,PermissionsMixin):
        
        email = models.EmailField(max_length=100)
        username = models.CharField(max_length=50)
        designation = models.CharField(max_length=100)
        phone_number = models.CharField(max_length=15)

        is_active = models.BooleanField(default=True)
        is_superuser = models.BooleanField(default=False)
        is_staff = models.BooleanField(default=False)

        date_joined = models.DateTimeField(default=timezone.now)
        last_login = models.DateTimeField(blank=True, null=True)

        objects=CustomerUserManager()

        USERNAME_FIELD= 'email'
        REQUIRED_FIELDS = ['username']

        class Meta:
            verbose_name= 'User'
            verbose_name_plural = 'Users'

        def get_full_name(self):
            return self.name

        def get_short_name(self):
            return self.name or self.email.split('@')[0]    

        groups = models.ManyToManyField(
        'auth.Group',
        related_name='official_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

        user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='official_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )




    



    
    




