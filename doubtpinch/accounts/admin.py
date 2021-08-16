from django.contrib import admin
from .models import User, UserSkill, Skill


admin.site.register(User)
admin.site.register(UserSkill)
admin.site.register(Skill)

