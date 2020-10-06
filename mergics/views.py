from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView

from ndh.mixins import NDHFormMixin

from . import forms, models

###########
# Helpers


class UserListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return self.model._default_manager.filter(user=self.request.user)


class UserCreateView(NDHFormMixin, LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class UserDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


#########
# Views


class InputListView(UserListView):
    model = models.ICSInput


class InputCreateView(UserCreateView):
    model = models.ICSInput
    fields = ['url']


class OutputListView(UserListView):
    model = models.ICSOutput


class OutputCreateView(UserCreateView):
    form_class = forms.OutputForm

    def get_form_kwargs(self):
        return {'user': self.request.user, **super().get_form_kwargs()}


class OutputDetailView(UserDetailView):
    model = models.ICSOutput


def ics(request, username, slug):
    user = get_object_or_404(User, username=username)
    output = get_object_or_404(models.ICSOutput, user=user, slug=slug)
    response = HttpResponse(content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="{user}-{slug}.csv"'
    response.write(output.to_ical())
    return response
