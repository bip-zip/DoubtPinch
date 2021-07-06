from .models import Notification

def navbar(request):
    if not request.user.is_anonymous:
        user=request.user
        notifications = Notification.objects.filter(user=user).order_by('-id')[:5]
        noti_count = Notification.objects.filter(user=user, is_seen=False).count()
        return {'notifications': notifications,'noti_count':noti_count}
    return {'notifications': '0','noti_count':0}
    



# from .models import Page

# def show_pages_menu(context):
#     pages_menu = Page.objects.filter(show_in_menu=True)
#     return {'pages_menu': pages_menu}