# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.models import User

from django.contrib import messages, auth
from .forms import AnswerForm
from .models import Question, QuestionsTags, Answer


# class QuestionDetailView(DetailView):
#
#     model = Question
#     template_name = 'question_detail.html'
#
#
#
#     def get_context_data(self, **kwargs):
#         context = {}
#         context['answerpost'] = AnswerForm()
#         return context

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

    #

# def AnswerSubmit(request, *args, **kwargs):
#     print(request)
#     priorURL = request.META.get('HTTP_REFERER')
#     form = AnswerForm(request.POST or None)
#     print(form)
#     print("ici")
#     if form.is_valid():
#         # pour enregistrer et relier un Answer à un user et à un Question
#         # il faut pour cela instancier l'user et l'Question
#         form.instance.question = Question.objects.get(pk=kwargs['pk'])
#         form.instance.user = request.user
#         form.save()
#         messages.success(request, "Vous avez bien créé une réponse !")
#         return redirect(priorURL)
#     else:
#         messages.error(request, "Petit problemo ...!")
#         return redirect(priorURL)


