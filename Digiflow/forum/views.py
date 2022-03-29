# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .forms import UserRegistrationForm, UserLoginForm, TagForm, AnswerForm

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

class FollowingListOfUser(DetailView):
    model = Profiles
    template_name = 'following.html'
    print(Profiles.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following'] = Profiles.objects.all()
        print(context)
        return context

class FollowerListOfUser(DetailView):
    model = Profiles
    template_name = 'follower.html' #object.follower.all, object.following.all dans template in for loop
    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['follower_'] = Profile.objects.all()
        return context"""



class UserRegistrationView(View):
    template_name = "user_registration_form.html"

    def get(self, request):
        context = {}
        context['form'] = UserRegistrationForm()
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            # do something
            pass
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        context = {}
        context['form'] = UserRegistrationForm()
        if username == '':
            messages.error(request, "Vous n'avez pas rempli de userName")
            return render(request, self.template_name, context)
        elif (password1 == '') | (password2 == ''):
            messages.error(request, "Vous n'avez pas rempli les champs de password")
            return render(request, self.template_name, context)
        elif password1 != password2:
            messages.error(request, "Les deux password sont différents")
            return render(request, self.template_name, context)
        elif User.objects.filter(username=username).exists():
            messages.error(request, "nom d'utilisateur existant")
            return render(request, self.template_name, context)
        elif User.objects.filter(email=email).exists():
            messages.error(request, "L'email existe déjà")
            return render(request, self.template_name, context)
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Enregistré avec succès")
            auth.login(request, user)

            return redirect('forum:login')


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    template_name = "user_login_form.html"

    def get(self, request):
        context = {}
        context['form'] = UserLoginForm()
        return render(request, self.template_name, context)


    def post(self, request):
        form = UserLoginForm(request.POST or None)
        username = request.POST['username']
        password = request.POST['password']

        context = {}
        context['form'] = UserLoginForm()
        if username == '':
            messages.error(request, "Vous n'avez pas rempli de userName")
            return render(request, self.template_name, context)
        elif password == '':
            messages.error(request, "Vous n'avez pas rempli de password")
            return render(request, self.template_name, context)
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Connecté avec succès")
                return redirect('forum:home')
            else:
                messages.error(request, "Utilisateur non trouvé")
                # param1= request, parm2=template, param3=context
                return render(request, self.template_name, context)


def ConnectAjax(request, *args, **kwargs):
    print('we went throught')
    form = UserLoginForm(request.POST or None)
    username = form.data.get('username')
    password = form.data.get('password')
    if username == '':
        messages.error(request, "Vous n'avez pas rempli de userName")
        return JsonResponse({'data':'true'})
    elif password == '':
        messages.error(request, "Vous n'avez pas rempli de password")
        return JsonResponse({'data': 'true'})
    else:
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Connecté avec succès")
            return JsonResponse({'data': 'true'})
        else:
            messages.error(request, "Utilisateur non trouvé")
            # param1= request, parm2=template, param3=context
            return JsonResponse({'data': 'true'})


class HomeView(ListView):
    model = Question
    template_name = "home.html"

class TagView(ListView):
    model = Question
    template_name = 'tag_list.html'

    def get_context_data(self, **kwargs):
        for each in Tag.objects.all():
            each.save()
        filtrage = Question.objects.filter(tags__slug=self.kwargs['slug'])
        context = super(TagView, self).get_context_data(object_list=filtrage, **kwargs)
        context['questions'] = filtrage
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        context['number'] = len(filtrage)
        return context

class TagCreateView(CreateView):
    model = Tag
    template_name = 'tag_form.html'
    form_class = TagForm

    def post(self, request, *args, **kwargs):
        form= TagForm(request.POST or None)
        form.save()
        return render(request, 'home.html', context={"form": form})




