from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from django.contrib import messages
from . import models
from . import forms

# to get the current user
from django.contrib.auth import get_user_model
User = get_user_model()


class BroadcastList(SelectRelatedMixin, generic.ListView):
    model = models.Broadcast
    select_related = ('user', 'planety')


class UserBroadcasts(generic.ListView):
    model = models.Broadcast
    template_name = 'broadcasts/user_broadcast_list.html'

    def get_queryset(self):
        try:
            self.broadcast_user = User.objects.prefetch_related(
                "broadcasts").get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.broadcast_user.broadcasts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["broadcast_user"] = self.broadcast_user
        return context


class BroadcastDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Broadcast
    select_related = ('user', 'planety')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreateBroadcast(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('title', 'message', 'planety')
    model = models.Broadcast

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)


class DeleteBroadcast(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):

    model = models.Broadcast
    select_related = ('user', 'planety')
    success_url = reverse_lazy('broadcasts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Broadcast Deleted')
        return super().delete(*args, **kwargs)
