# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.models import User

from django.contrib import messages, auth
from .forms import AnswerForm
from .models import Question, QuestionsTags, Answer, Vote_Answer, Vote_Question


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