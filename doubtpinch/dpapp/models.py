from django.db import models
from accounts.models import User
from datetime import datetime


class Doubt(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.TextField(null=False)
    description=models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    tags=models.CharField(max_length=255, null=True)
    views= models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def total_replies(self):
        totalreplies = Answer.objects.filter(doubt=self).count()
        return totalreplies


class Answer(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='answerer')
    doubt=models.ForeignKey(Doubt,on_delete=models.CASCADE)
    description=models.TextField(null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    updated=models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    @property
    def actual_vote(self):
        rightvote = RightPoint.objects.filter(answer=self).count()
        wrongvote = WrongPoint.objects.filter(answer=self).count()
        actualvote=rightvote - wrongvote
        return actualvote
    
  


class Comment(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name='commentor')
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE, null=True)
    description=models.TextField(null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    updated=models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

class RightPoint(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name='rp')
    answer= models.ForeignKey(Answer,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

class WrongPoint(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name='wp')
    answer= models.ForeignKey(Answer,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name