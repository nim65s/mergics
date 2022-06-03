from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ndh.mixins import NDHFormMixin

from . import forms, models

###########
# Helpers


class UserQuerysetMixin:
    def get_queryset(self):
        # return self.model._default_manager.filter(user=self.request.user)
        return super().get_queryset().filter(user=self.request.user)


class UserFormKwargsMixin:
    def get_form_kwargs(self):
        return {"user": self.request.user, **super().get_form_kwargs()}


class UserListView(LoginRequiredMixin, UserQuerysetMixin, ListView):
    pass


class UserCreateView(NDHFormMixin, LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(NDHFormMixin, LoginRequiredMixin, UserQuerysetMixin, UpdateView):
    pass


class UserDetailView(LoginRequiredMixin, UserQuerysetMixin, DetailView):
    pass


#########
# Views


class InputListView(UserListView):
    model = models.ICSInput


class InputCreateView(UserCreateView):
    model = models.ICSInput
    fields = ["url"]


class OutputListView(UserListView):
    model = models.ICSOutput


class OutputCreateView(UserFormKwargsMixin, UserCreateView):
    form_class = forms.OutputForm


class OutputUpdateView(UserFormKwargsMixin, UserUpdateView):
    form_class = forms.OutputForm
    model = models.ICSOutput


class OutputDetailView(UserDetailView):
    model = models.ICSOutput


def ics(request, username, slug):
    user = get_object_or_404(User, username=username)
    output = get_object_or_404(models.ICSOutput, user=user, slug=slug)
    response = HttpResponse(content_type="text/calendar")
    response["Content-Disposition"] = f'attachment; filename="{user}-{slug}.ics"'
    response.write(output.to_ical())
    return response
