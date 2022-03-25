from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *

"""def profile(request):
    profile = Profiles.objects.all()

    return render(request,'profile.html', {'profile':profile})"""


class ProfileDetailView(DetailView):
    model = Profiles
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amies'] = Friendship.objects.all().count()
        context['question'] = Question.objects.all().order_by('created_at')
        context['answer'] = Answer.objects.all().order_by('created_at')
        return context


