from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from apps.messages.models import Thread, Message


class Chat(TemplateView):
    template_name = 'messages/chat.html'

    def get_context_data(self, *args, **kwargs):
        pk = kwargs.get('pk')

        thread = get_object_or_404(Thread, pk=pk, participants=self.request.user)

        messages = thread.message_set.order_by("-datetime")[:100]
        messages_total = thread.message_set.count()

        partner = thread.participants.exclude(id=self.request.user.id)[0]

        context = {
            'thread': thread,
            "thread_messages": messages,
            'messages_total': messages_total,
            'messages_sent': 0,
            'messages_received': 0,
            'partner': partner,
        }

        return context


class Messages(TemplateView):
    model = Thread
    template_name = "messages/messages.html"

    def get_context_data(self, *args, **kwargs):
        #context = super(Messages, self).get_context_data(**kwargs)
        threads = Thread.objects.filter(participants=self.request.user).order_by("-last_message")

        for thread in threads:
            thread.partner = thread.participants.exclude(id=self.request.user.id)[0]
            thread.total_messages = Thread.objects.filter(participants=self.request.user).count()

        context = {
            'threads': threads
        }

        return context

    def post(self, request, *args, **kwargs):

        message_text = request.POST.get("message")[:10000]

        if not message_text:
            return HttpResponse("No message found")

        recipient_name = request.POST.get("recipient_name")
        recipient = get_object_or_404(User, username=recipient_name)

        if recipient == request.user:
            return HttpResponse("You cannot send messages to yourself.")

        thread_queryset = Thread.objects.filter(
            participants=recipient).filter(
                participants=request.user
            )

        if thread_queryset.exists():
            thread = thread_queryset[0]
        else:
            thread = Thread.objects.create()
            thread.participants.add(request.user, recipient)

        Message.objects.create(
            text=message_text,
            thread=thread,
            sender=request.user
        )

        return HttpResponseRedirect(reverse("messages"))
