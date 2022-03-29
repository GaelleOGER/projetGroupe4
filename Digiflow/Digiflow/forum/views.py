from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *

"""def profile(request):
    profile = Profiles.objects.all()

    return render(request,'profile.html', {'profile':profile})"""


class ProfiCreatetView(CreateView):
    model = Profiles
    template_name = "create_profile.html"
    fields = ['first_name', 'last_name', 'image', 'bio']

    """def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)"""

class ProfileDetailView(DetailView):
    model = Profiles
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        context['amies'] = auth.userprofile.friendlist.count()
        context['question'] = Question.objects.filter(profile=self.kwargs['pk']).order_by('created_at')
        context['answer'] = Answer.objects.filter(profile=self.kwargs['pk']).order_by('created_at')
        context['date_joind'] = auth.date_joined
        return context


class ProfileListView(ListView):
    model = Profiles
    template_name = "profile_list.html"


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        id_auth = self.request.user.id
        context['profile_list'] = Profiles.objects.exclude(user__id=id_auth)
        return context






"""class AjouteAmieCreateView(CreateView):
    model = Friendship
    template_name = "profile_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profiles.objects.all()
        return context"""




class ProfileUpdateView(UpdateView):
    model = Profiles
    template_name = 'profile_update.html'
    fields = ['first_name', 'last_name', 'image', 'bio', 'points']

    """def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)"""

def AddAmie (request, *args, **kwargs):

    priorURL = request.META.get('HTTP_REFERER')
    user_cliquer = User.objects.get(id=kwargs['pk'])
    id_user = request.user
    print(' vous êtes bien passé au bon endroit ')
    print('plus qua ajouter les conditions')
    if user_cliquer in request.user.userprofile.friendlist.all():
        request.user.userprofile.friendlist.remove(user_cliquer)
        request.user.userprofile.save()
    else:
        request.user.userprofile.friendlist.add(user_cliquer)
        request.user.userprofile.save()
    '''
    for each in Profiles.objects.all():
        each.points = 500
        each.save()
        '''
    return redirect(priorURL)