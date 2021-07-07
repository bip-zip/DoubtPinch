from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Doubt, Answer,RightPoint,WrongPoint,Notification,Comment

# Apply summernote to all TextField in model.
class DoubtAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    exclude=('created_on',)
    list_display=('user','title','tags',)
    list_display_links=('user','title',)
    search_fields=('title',)
    list_per_page =25
    summernote_fields = ('description')


class AnswerAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    exclude=('created_on',)
    list_display=('user','doubt','updated',)
    list_display_links=('user','doubt',)
    search_fields=('doubt',)
    list_per_page =25
    summernote_fields = ('description')



admin.site.register(Doubt, DoubtAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(RightPoint)
admin.site.register(WrongPoint)
admin.site.register(Notification)
admin.site.register(Comment)

