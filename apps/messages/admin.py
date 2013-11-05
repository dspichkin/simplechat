#coding: utf-8
from django.contrib import admin
from apps.messages.models import Thread, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 1


class ThreadAdmin(admin.ModelAdmin):
    inlines = [MessageInline]

admin.site.register(Thread, ThreadAdmin)
#admin.site.register(Message)

