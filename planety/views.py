from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from planety.models import Planety, PlanetyMember
from django.shortcuts import get_object_or_404
from . import models


class CreatePlanety(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Planety


class SinglePlanety(generic.DetailView):
    model = Planety


class ListPlanety(generic.ListView):
    model = Planety


class JoinPlanety(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('planety:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        planety = get_object_or_404(Planety, slug=self.kwargs.get('slug'))

        try:
            PlanetyMember.objects.create(
                user=self.request.user, planety=planety)

        except IntegrityError:
            messages.warning(self.request, 'Warning  already a member!')

        else:
            messages.success(self.request, 'You are now a member!')

        return super().get(request, *args, **kwargs)


class LeavePlanety(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('planety:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.PlanetyMember.objects.filter(
                user=self.request.user,
                planety__slug=self.kwargs.get('slug')
            ).get()
        except models.PlanetyMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group')
        else:
            membership.delete()
            messages.success(self.request, "You have left the group!")
        return super().get(request, *args, **kwargs)
