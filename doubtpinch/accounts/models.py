
from django.db import models
from django.contrib.auth.models import AbstractUser#, UserManager
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    username = None#models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    profile_pic= models.ImageField(upload_to='admin_pics', null=True, blank=True)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    email_confirmed = models.BooleanField(default=False) #initially this field is false but will se chan
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    description=models.TextField(null=True)

 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] #emaila nd password are required fields and first name and last name is inherited from the user creation model

    #instanciate the usermanager object
    object = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    @property
    def ProfilePicUrl(self):
        try:
            url=self.profile_pic.url
        except:
            url=''
        return url
   

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
       

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    
    @property
    def apr_count(self):
        from dpapp.models import Doubt, Answer, RightPoint, WrongPoint
        total_apr=0
        all_answer= Answer.objects.filter(user=self)
        answercount= Answer.objects.filter(user=self).count()
        total_apr=answercount*5
        for i in all_answer:
            answer=Answer.objects.get(id=i.id)
            right=RightPoint.objects.filter(answer=answer).count()
            wrong=WrongPoint.objects.filter(answer=answer).count()
            total_apr=total_apr+(right*3)-(wrong)
        return total_apr



    #

    
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    #
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.is_staff
    #
    # @property
    # def is_admin(self):
    #     "Is the user a admin member?"
    #     return self.is_admin
    #
    # @property
    # def is_active(self):
    #     "Is the user active?"
    #     return self.is_active
class Skill (models.Model):
    skill=models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.skill

class UserSkill(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    skill=models.ForeignKey(Skill,on_delete=models.CASCADE)
    level=models.CharField(max_length=30,null=True)

    def __str__(self):
        return str(self.skill + self.user)