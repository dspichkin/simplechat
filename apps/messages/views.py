from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from apps.messages.utils import send_message
from apps.messages.models import Thread


class SendMessage(TemplateView):
    """
        Send message via Django
    """
    def post(self, request, *args, **kwargs):

        message_text = request.POST.get("message")[:10000]

        if not message_text:
            return HttpResponse("No message found")

        recipient_name = request.POST.get("recipient_name")
        recipient = get_object_or_404(User, usrename=recipient_name)

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

        send_message(
            thread.id,
            request.user.id,
            message_text,
            request.user.username
        )

        return HttpResponseRedirect(reverse("apps.messages.views.Messages"))


class Messages(TemplateView):
    model = Thread
    template_name = "messages/messages.html"

    def get_context_data(self, *args, **kwargs):
        #context = super(Messages, self).get_context_data(**kwargs)
        threads = Thread.objects.filter(participants=self.request.user).order_by("-last_message")

        #for thread in threads:
        #    thread.partner = thread.participants.exclude(id=self.request.user.id)[0]
        #    thread.total_messages = ""

        context = {
            'threads': threads
        }

        return context
