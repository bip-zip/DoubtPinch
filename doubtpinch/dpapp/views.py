from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView
from .models import Doubt, Answer, RightPoint, WrongPoint
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import DoubtForm, AnswerForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


class Home(ListView):
    template_name="dpapp/home.html"
    model= Doubt

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs) 
        doubts=Doubt.objects.all().order_by('-views')
        
       

        # order by max comments for a certain timestamp

        newdoubts=Doubt.objects.all().order_by('-id')
        paginator= Paginator(doubts, 2)
        page = self.request.GET.get('page')
        # blogs_final= paginator.get_page(page_number)

        try:
            doubts = paginator.page(page)
        except PageNotAnInteger:
            doubts = paginator.page(1)
        except EmptyPage:
            doubts = paginator.page(paginator.num_pages)

        context.update({'doubts':doubts,'newdoubts':newdoubts,'page':page})
        return context


class Detail(TemplateView):
    template_name="dpapp/detail.html"

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs) 
        doubt_id= self.kwargs['id']
        doubt=Doubt.objects.get(id=doubt_id)
        doubt.views = doubt.views + 1
        doubt.save()
        answers= Answer.objects.filter(doubt=doubt)
        
        paginator= Paginator(answers, 2)
        page = self.request.GET.get('page')
        # blogs_final= paginator.get_page(page_number)

        try:
            answers = paginator.page(page)
        except PageNotAnInteger:
            answers = paginator.page(1)
        except EmptyPage:
            answers = paginator.page(paginator.num_pages)
        context.update({'doubt':doubt,'answers':answers, 'form':AnswerForm, 'page':page})
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
        





        # editordata= request.POST.get('editordata')
        # user= self.request.user
        # doubt_id= self.kwargs['id']
        # doubt=Doubt.objects.get(id=doubt_id)
        # Answer.objects.create(user=user, doubt=doubt, description=editordata)
        


  
    
class Profile(TemplateView):
    template_name="dpapp/profile.html"


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
class Search(TemplateView):
    template_name="dpapp/search.html"

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs) 
        query = self.request.GET['query']
        
        doubts=Doubt.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)| Q(tags__icontains=query)).distinct()
        counted=Doubt.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)| Q(tags__icontains=query)).distinct().count()
       
        paginator= Paginator(doubts,2)
        page = self.request.GET.get('page')
        # blogs_final= paginator.get_page(page_number)

        try:
            doubts = paginator.page(page)
        except PageNotAnInteger:
            doubts = paginator.page(1)
        except EmptyPage:
            doubts = paginator.page(paginator.num_pages)
        context.update({'counted':counted,'doubts':doubts, 'form':AnswerForm, 'page':page})
        return context

   
        
