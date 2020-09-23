from django.contrib import admin
from .models import Post, Group, GroupMessage
# Register your models here.
admin.site.register(Post)
admin.site.register(Group)
admin.site.register(GroupMessage)