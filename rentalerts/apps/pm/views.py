from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.utils.functional import cached_property
from django.contrib import messages


from rentalerts.apps.accounts.decorators import login_required
from rentalerts.apps.apartments.models import Apartment
from rentalerts.apps.helpers.utils.email import send_email_from_template
from rentalerts.apps.pm.models import Message
from rentalerts.apps.pm.forms import MessageForm, ReplyMessageForm


@login_required
class ReceivedMessageList(ListView):

    template_name = "pm/received_messages.html"

    def get_queryset(self):
        return self.request.user.received_messages.all()


@login_required
class SentMessageList(ListView):

    template_name = "pm/sent_messages.html"

    def get_queryset(self):
        return self.request.user.sent_messages.all()


@login_required
class CreateMessage(CreateView):

    model = Message
    form_class = MessageForm

    @cached_property
    def apartment(self):

        return get_object_or_404(
            Apartment, 
            pk=self.kwargs['apartment_id']
        )
    
    def get_context_data(self, **kwargs):

        context = super(CreateMessage, self).get_context_data(**kwargs)
        context['apartment'] = self.apartment
        return context

    def form_valid(self, form):

        message = form.save(commit=False)
        message.apartment = self.apartment
        message.receiver = message.apartment.tenant
        message.sender = self.request.user
        message.save()

        messages.success(self.request, "Your message has been sent")

        send_email_from_template(
            subject=message.subject,
            recipient_list=[message.receiver.email],
            template="pm/emails/message.txt",
            context=RequestContext(self.request, {
                'message' : message,
                })
        )

        return redirect(message.apartment.get_absolute_url())


@login_required
class Reply(CreateView):

    model = Message
    form_class = ReplyMessageForm
    template_name = "pm/message_form.html"

    @cached_property
    def parent(self):

        return get_object_or_404(
            self.request.user.received_messages,
            pk=self.kwargs['parent_id']
        )
    
    def get_initial(self):
        initial = super(Reply, self).get_initial()
        initial['subject'] = "RE:%s" % self.parent.subject
        return initial

    def get_context_data(self, **kwargs):

        context = super(Reply, self).get_context_data(**kwargs)
        context['parent'] = self.parent
        return context

    def form_valid(self, form):

        message = form.save(commit=False)
        message.parent = self.parent
        message.apartment = self.parent.apartment
        message.receiver = self.parent.sender
        message.sender = self.request.user

        message.save()

        messages.success(self.request, "Your message has been sent")

        send_email_from_template(
            subject=message.subject,
            recipient_list=[message.receiver.email],
            template="pm/emails/message.txt",
            context=RequestContext(self.request, {
                'message' : message,
            })
        )

        return redirect("pm:sent_list")


@login_required
class MessageDetail(DetailView):

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) |  Q(
                receiver=self.request.user
            )
        )

    def get(self, request, *args, **kwargs):

        response = super(MessageDetail, self
            ).get(request, *args, **kwargs)

        if self.object.receiver == self.request.user:
            self.object.is_read = False
            self.object.save()


        return response

    def get_context_data(self, **kwargs):

        context = super(MessageDetail, self).get_context_data(**kwargs)

        if self.object.receiver == self.request.user:

            form = ReplyMessageForm(
                form_action=self.object.get_reply_url(),
                initial={'subject' : 'RE:%s' % self.object.subject}
            )
            context['form'] = form 

        return context


