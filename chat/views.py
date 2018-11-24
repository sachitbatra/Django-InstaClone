from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.views.generic import DetailView, ListView
from authentication.views import get_user
from .forms import ComposeForm
from .models import Thread, ChatMessage

class InboxView(ListView):
    template_name = 'inbox.html'

    def get_queryset(self):
        if get_user(self.request) is not None:
            user = get_user(self.request)
            return Thread.objects.by_user(user)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if get_user(self.request) is not None:
            curUser = get_user(self.request)
            context['curUser'] = curUser.email_address
        return context

    def dispatch(self, request, *args, **kwargs):
        if get_user(request) is None:
            messages.error(request, 'Please log in first to access Inbox.')
            return HttpResponseRedirect('/')
        else:
            return super(InboxView, self).dispatch(request, *args, **kwargs)


class ThreadView(FormMixin, DetailView):
    template_name = 'thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        user = None
        if get_user(self.request) is not None:
            user = get_user(self.request)
        return Thread.objects.by_user(user)

    def get_object(self):
        other_username = self.kwargs.get("username")
        if get_user(self.request) is not None:
            user = get_user(self.request)

        obj, created = Thread.objects.get_or_new(user, other_username)
        if obj is None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        if get_user(self.request) is not None:
            curUser = get_user(self.request)
            context['curUser'] = curUser.email_address

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = None

        if get_user(self.request) is not None:
            user = get_user(self.request)

        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if get_user(request) is None:
            messages.error(request, 'Please log in first to access Inbox.')
            return HttpResponseRedirect('/login')
        else:
            return super(ThreadView, self).dispatch(request, *args, **kwargs)
