from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.urls.conf import re_path
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from .models import Doubt, Answer, RightPoint, WrongPoint, Comment,Notification,TaggableManager
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import DoubtForm, AnswerForm, CommentForm, ProfileForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from accounts.models import User, UserSkill, Skill
# from .documents import DoubtDocument
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class Home(ListView):
    template_name="dpapp/home.html"
    model= Doubt
    
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs) 
        doubts=Doubt.objects.all().order_by('-views')
        newdoubts=Doubt.objects.all().order_by('-id')
        paginator= Paginator(doubts, 10)
        page = self.request.GET.get('page')

        try:
            doubts = paginator.page(page)
        except PageNotAnInteger:
            doubts = paginator.page(1)
        except EmptyPage:
            doubts = paginator.page(paginator.num_pages)

        context.update({'doubts':doubts,'newdoubts':newdoubts,'page':page})
        return context

@method_decorator(login_required, name='dispatch')
class Detail(TemplateView):
    template_name="dpapp/detail.html"

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs) 
        doubt_id= self.kwargs['id']
        doubt=Doubt.objects.get(id=doubt_id)
        doubt.views = doubt.views + 1
        doubt.save()
        answers= Answer.objects.filter(doubt=doubt)
        tags = doubt.tags.all()
        print(tags)
        related_question=Doubt.objects.filter(tags__in=tags).exclude(id=(doubt.id))[:15]
        paginator= Paginator(answers, 2)
        page = self.request.GET.get('page')
        try:
            answers = paginator.page(page)
        except PageNotAnInteger:
            answers = paginator.page(1)
        except EmptyPage:
            answers = paginator.page(paginator.num_pages)
        context.update({'doubt':doubt,'answers':answers, 'form':AnswerForm, 
                        'page':page,'related_question':related_question})
        return context

    def post(self, request, **kwargs):
        form=AnswerForm(request.POST)
        user=self.request.user
        doubt_id= self.kwargs['id']
        doubt=Doubt.objects.get(id=doubt_id)
        if form.is_valid():
            form.instance.doubt=doubt
            form.instance.user=user
            form.save()
            return HttpResponseRedirect(self.request.path_info)
        return HttpResponseRedirect(self.request.path_info)        



from itertools import chain
from operator import attrgetter

@method_decorator(login_required, name='dispatch')
class Profile(TemplateView):
    template_name="dpapp/profile.html"

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs) 
        user=self.request.user
        useremail=user.email
        user=User.objects.get(email=useremail)
        total_replies=Answer.objects.filter(user=user).count()
        total_upvotes=RightPoint.total_upvotes_of_answerer(self,user)
        skill=Skill.objects.all()
        userskill=UserSkill.objects.filter(user=user)
        qs1 = Doubt.objects.filter(user=user) #first qs
        qs2 = Answer.objects.filter(user=user) #second qs
        recent_activity = sorted(chain(qs1,qs2),key=attrgetter('created_on'),)
        paginator= Paginator(recent_activity, 3)
        page = self.request.GET.get('page')

        try:
            recent_activity = paginator.page(page)
        except PageNotAnInteger:
            recent_activity = paginator.page(1)
        except EmptyPage:
            recent_activity = paginator.page(paginator.num_pages)

        form= ProfileForm(instance=user)
        context.update({ 'form':form,'recent_activity':recent_activity,
                        'total_upvotes':total_upvotes,'total_replies':total_replies,
                        'skill':skill,'userskill':userskill})
        return context

    def post(self, request, **kwargs):
        user=self.request.user
        useremail=user.email
        user=User.objects.get(email=useremail)

        form=ProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            if request.FILES == '':
                form.save()
                return HttpResponseRedirect(self.request.path_info)
            # form.instance.email=email
            form.save()
            return HttpResponseRedirect(self.request.path_info)
        return HttpResponseRedirect(self.request.path_info)
    
        
@method_decorator(login_required, name='dispatch')
class PostDoubtView(CreateView):
    model = Doubt
    template_name = "dpapp/addDoubt.html"
    form_class = DoubtForm
    success_url='dpapp:profile'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user= self.request.user
        self.object.user=user
        self.object.save()
        form.save_m2m()

        return redirect('dpapp:profile')






# from django_summernote.widgets import SummernoteInplaceWidget
# class PostDoubtView(CreateView):
#     model = Doubt
#     template_name = "dpapp/addDoubt.html"
#     fields = ['title', 'description']

#     def get_form(self, form_class=None):
#         form = super(PostDoubtView, self).get_form(form_class)
#         form.fields['description'].widget = SummernoteInplaceWidget()
#         return form
    
    
def saveRPoint(request):
    if request.method == "POST":
        answerid=request.POST['answer_id']
        answer=Answer.objects.get(id=answerid)
        user=request.user
        actualVote=answer.actual_vote
        checkRight= RightPoint.objects.filter(answer=answer, user=user)
        checkWrong= WrongPoint.objects.filter(answer=answer, user=user)
        if checkRight.count() > 0 :
            checkRight.delete()
            actualVote=answer.actual_vote
            return JsonResponse({'bool':True,'actualVote':actualVote})

        elif checkWrong.count() > 0 :
            checkWrong.delete()
            RightPoint.objects.create(
                answer=answer,
                user=user)
            actualVote=answer.actual_vote
            return JsonResponse({'bool':True,'actualVote':actualVote})
        else:
            RightPoint.objects.create(
                answer=answer,
                user=user)
            actualVote=answer.actual_vote
            return JsonResponse({'bool':True,'actualVote':actualVote})


def saveWPoint(request):
    if request.method == "POST":
        answerid=request.POST['answer_id']
        answer=Answer.objects.get(id=answerid)
        user=request.user
        actualVote=answer.actual_vote
        checkRight= RightPoint.objects.filter(answer=answer, user=user)
        checkWrong= WrongPoint.objects.filter(answer=answer, user=user)
        if checkWrong.count() > 0:
            checkWrong.delete()
            actualVote=answer.actual_vote
            return JsonResponse({'bool':True,'actualVote':actualVote})

        elif checkRight.count() > 0 :
            checkRight.delete()
            WrongPoint.objects.create(
                answer=answer,
                user=user)
            actualVote=answer.actual_vote
            return JsonResponse({'bool':True,'actualVote':actualVote})
        else:
            WrongPoint.objects.create(
                answer=answer,
                user=user)
            actualVote=answer.actual_vote
            return JsonResponse({'bool':True,'actualVote':actualVote})


from django.db.models import Q
@method_decorator(login_required, name='dispatch')
class Search(TemplateView):
    template_name="dpapp/search.html"

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs) 
        query = self.request.GET['query']
        doubts=Doubt.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)| 
                Q(tags__name__icontains=query)).distinct()
        counted=doubts.count()
        paginator= Paginator(doubts,2)
        page = self.request.GET.get('page')

        try:
            doubts = paginator.page(page)
        except PageNotAnInteger:
            doubts = paginator.page(1)
        except EmptyPage:
            doubts = paginator.page(paginator.num_pages)
        context.update({'counted':counted,'doubts':doubts, 'form':AnswerForm, 'page':page})
        # context.update({'counted':counted,'doubts':doubts, 'form':AnswerForm})

        return context

   
@method_decorator(login_required, name='dispatch')
class CommentView(TemplateView):
    template_name="dpapp/comments.html"

    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs) 
        answer_id= self.kwargs['id']
        answer= Answer.objects.get(id=answer_id)
        comments= Comment.objects.filter(answer=answer)
        paginator= Paginator(comments,10)
        page = self.request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        context.update({'comments':comments,'answer':answer, 'form':CommentForm, 'page':page})
        return context
    

    def post(self, request, **kwargs):
        form=CommentForm(request.POST)
        user=self.request.user
        answer_id= self.kwargs['id']
        answer=Answer.objects.get(id=answer_id)
        if form.is_valid():
            form.instance.answer=answer
            form.instance.user=user
            form.save()
            return HttpResponseRedirect(self.request.path_info)
        return HttpResponseRedirect(self.request.path_info)

@method_decorator(login_required, name='dispatch')
class NotificationView(TemplateView):
    template_name= 'dpapp/notifications.html'

    def get_context_data(self, **kwargs):
        context = super(NotificationView, self).get_context_data(**kwargs) 
        user=self.request.user
        notifications = Notification.objects.filter(user=user).order_by('-id')
        noti_count = Notification.objects.filter(user=user, is_seen=False).count()
        paginator= Paginator(notifications, 15)
        page = self.request.GET.get('page')
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)
        context.update({'notifications': notifications,'noti_count':noti_count,'page':page})
        return context

def notification_seen(request):
    if request.method == "POST":
        notification_id=request.POST['notification_id']
        notification=Notification.objects.get(id=notification_id)
        user=request.user
        if notification.is_seen == True:
            notificationCount= Notification.objects.filter(user=user, is_seen=False).count()
            return JsonResponse({'bool':True,'notificationCount':notificationCount})
        notification.is_seen=True
        notification.save()
        notificationCount= Notification.objects.filter(user=user, is_seen=False).count()
        return JsonResponse({'bool':True,'notificationCount':notificationCount})

@method_decorator(login_required, name='dispatch')
class TagsView(TemplateView):
    template_name="dpapp/tags.html"

    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs) 
        doubts=Doubt.objects.filter(tags__slug=self.kwargs.get('slug'))
        counted=Doubt.objects.filter(tags__slug=self.kwargs.get('slug')).count()
        tagname=self.kwargs.get('slug')
        paginator= Paginator(doubts,2)
        page = self.request.GET.get('page')

        try:
            doubts = paginator.page(page)
        except PageNotAnInteger:
            doubts = paginator.page(1)
        except EmptyPage:
            doubts = paginator.page(paginator.num_pages)
        context.update({'counted':counted,'doubts':doubts, 'page':page, 'tagname':tagname})
        return context

from django.http import HttpResponseNotFound
class UpdateAnswer(UpdateView):
    form_class=AnswerForm
    model=Answer

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return HttpResponseNotFound("You are not allowed to edit this Post")
        return super(UpdateAnswer, self).dispatch(request, *args, **kwargs)
    
class DeleteAnswer(View):
    def get(self, request, **kwargs):
        ansid=self.kwargs['id']
        Answer.objects.get(id=ansid).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def dispatch(self, request, *args, **kwargs):
        ansid=self.kwargs['id']
        obj=Answer.objects.get(id=ansid)
        if obj.user != self.request.user:
            return HttpResponseNotFound("You are not allowed to delete.")
        return super(DeleteAnswer, self).dispatch(request, *args, **kwargs)
    

# export ES_JAVA_OPTS="-Xms256m -Xmx256m"


# python3 manage.py search_index --rebuild