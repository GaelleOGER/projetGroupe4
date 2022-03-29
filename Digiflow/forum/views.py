# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.models import User

from django.contrib import messages, auth
from .forms import AnswerForm

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


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnswerForm()
        context['answer'] = Answer.objects.filter(question__pk=self.kwargs['pk'])

        return context


def AnswerSubmit(request, *args, **kwargs):
    priorURL = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            form.instance.question = Question.objects.get(id=kwargs['id'])
            form.instance.user = request.user
            form.save()  # On sauvegarde le formulaire
            messages.success(request, 'réponse publié')
            return redirect(priorURL)
    else:
        messages.error(request, 'réponse non publié')
        form = AnswerForm()

    return render(request, 'question_detail.html', context={"form": form})

# nous avons deux vue qui nous permettent de défenir si c 'est une question ou une réponse
# donc deux url et relatif
# pour les question reverse d'url dans la template avec l'id de la question
# et la meme chose pour les reponse


def ChangeVoteReponse(request, *args, **kwargs):
    priorURL = request.META.get('HTTP_REFERER')
    question = Question.objects.get(id=kwargs['pk'])
    toi = request.user

    if toi == question.user:
        # rajouter le message comm quoi on ne peut pas voté sa propre question
        return redirect(priorURL)
    if toi in question.questionvote.profile.all():
        question.questionvote.profile.remove(toi)
    else:
        question.questionvote.profile.add(toi)
    return redirect(priorURL)


def ChangeVoteAnswer(request, *args, **kwargs):
    priorURL = request.META.get('HTTP_REFERER')
    answer = Answer.objects.get(id=kwargs['pk'])
    toi = request.user

    if toi == answer.user:
        # rajouter le message comm quoi on ne peut pas voté sa propre question
        return redirect(priorURL)
    if toi in answer.answervote.profile.all():
        answer.answervote.profile.remove(toi)
    else:
        answer.answervote.profile.add(toi)
    return redirect(priorURL)


def home(request, *args, **kwargs):
    return HttpResponse('<h1>Bonjour</h1>')