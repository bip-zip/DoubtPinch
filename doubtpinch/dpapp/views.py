from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView
from .models import Doubt, Answer, RightPoint, WrongPoint
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import DoubtForm, AnswerForm


class Home(ListView):
    template_name="dpapp/home.html"
    model= Doubt

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs) 
        doubts=Doubt.objects.all().order_by('-id')

        context.update({'doubts':doubts})
        return context


class Detail(TemplateView):
    template_name="dpapp/detail.html"

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs) 
        doubt_id= self.kwargs['id']
        doubt=Doubt.objects.get(id=doubt_id)
        answers= Answer.objects.filter(doubt=doubt)
        context.update({'doubt':doubt,'answers':answers, 'form':AnswerForm})
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
