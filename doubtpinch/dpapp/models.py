from django.db import models
from accounts.models import User
from datetime import datetime

from taggit.managers import TaggableManager


class Doubt(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.TextField(null=False)
    description=models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    views= models.IntegerField(default=0)
    tags = TaggableManager()

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
    
    def user_replied_answer(sender, instance, *args, **kwargs):
        answer=instance
        doubt=answer.doubt
        sender=answer.user
        text_preview="{answerer} replied to your doubt.".format(answerer=sender.first_name)

        notify= Notification(doubt=doubt, sender=sender, user=doubt.user,text_preview=text_preview, notification_type=1)
        notify.save()
    
    # def user_replied_answer(sender, instance, *args, **kwargs):
    #     answer=instance
    #     doubt=answer.doubt
    #     sender=answer.user
    #     notify= Notification.objects.filter(doubt=doubt, sender=sender, notification_type=1)
    #     notify.delete()

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
    
    def user_replied_comment(sender, instance, *args, **kwargs):
        comment=instance
        answer=comment.answer
        sender=comment.user
        text_preview="{answerer} commented to your answer.".format(answerer=sender.first_name)

        notify= Notification(answer=answer, sender=sender, user=answer.user,text_preview=text_preview, notification_type=3)
        notify.save()

class RightPoint(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name='rp')
    answer= models.ForeignKey(Answer,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
    
    @staticmethod
    def total_upvotes_of_answerer(self,user):
        answer=Answer.objects.filter(user=user)
        upvotes=RightPoint.objects.filter(answer__in=answer).count()
        return upvotes



class WrongPoint(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name='wp')
    answer= models.ForeignKey(Answer,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


from django.db.models.signals import post_save
class Notification(models.Model):
    NOTIFICATION_TYPES = ((1,'Doubt'),(2,'Answer'), (3,'Comment'))

    doubt= models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name="noti_doubt", blank=True, null=True)
    answer= models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="noti_answer", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
	
    def __str__(self):
        return self.user.email



post_save.connect(Answer.user_replied_answer, sender=Answer)
post_save.connect(Comment.user_replied_comment, sender=Comment)
    