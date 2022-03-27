# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.models import User

from django.contrib import messages, auth
from .forms import AnswerForm
from .models import Question, QuestionsTags, Answer


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


def VoteQuestionSetter(request, *args, **kwargs):
    print(request)
    print(args)
    print(kwargs)
    id_question = Question.objects.get(id=kwargs['pk'])
    print(id_question)
    priorURL = request.META.get('HTTP_REFERER')

    # qs = Question.objects.get(pk=kwargs['pk'])
    # if request.user in qs.total_votes.all():
    #     qs.total_votes.remove(request.user)
    # else:
    #     qs.total_votes.add(request.user)

    return redirect(priorURL)


def VoteAnswerSetter(request, *args, **kwargs):

    priorURL = request.META.get('HTTP_REFERER')

    qs = Answer.objects.get(id=kwargs['id'])
    if request.user in qs.total_votes.all():
        qs.total_votes.remove(request.user)
    else:
        qs.total_votes.add(request.user)

    return redirect(priorURL)

def home(request , *args, **kwargs):
    return HttpResponse('<h1>Bonjour</h1>')