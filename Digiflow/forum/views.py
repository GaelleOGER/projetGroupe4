# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View

from .forms import UserRegistrationForm, UserLoginForm, TagForm, AnswerForm, QuestionForm

from django.contrib.auth import logout
from .models import *

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from api.serializers import TagFilterSlugModelSerializer

# Home


class HomeView(ListView):
    paginate_by = 5
    model = Question
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #afficher les 10 premiers elements
        context['tags'] = Tag.objects.all()[:10]
        context['questions'] = Question.objects.all()
        context['number'] = len(Question.objects.all())
        return context


# PROFILE
"""def profile(request):
    profile = Profile.objects.all()

    return render(request,'profile.html', {'profile':profile})"""



class ProfileCreateView(CreateView):
    model = Profile
    template_name = "create_profile.html"
    fields = ['first_name', 'last_name', 'image', 'bio']

    """def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)"""


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        context['amies'] = auth.userprofile.friendlist.count()
        context['question'] = Question.objects.filter(user=self.kwargs['pk']).order_by('created_at')
        context['answer'] = Answer.objects.filter(user=self.kwargs['pk']).order_by('created_at')
        context['date_joind'] = auth.date_joined
        return context


class ProfileListView(ListView):
    model = Profile
    template_name = "profile_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        id_auth = self.request.user.id
        context['profile_list'] = Profile.objects.exclude(user__id=id_auth)
        return context


"""class AjouteAmieCreateView(CreateView):
    model = Friendship
    template_name = "profile_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.all()
        return context"""


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    fields = ['first_name', 'last_name', 'bio', 'point']

    """def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)"""


# FRIEND


def AddFriendRelationship(request, *args,**kwargs):

    priorURL = request.META.get('HTTP_REFERER')
    object = Profile.objects.get(pk=kwargs['pk'])
    friend = Friend.objects.create(
        profile=request.user.userprofile,
        friend=object.user,
    )
    object.waitinglist.add(request.user)

    return redirect(priorURL)


def RemoveFriendRelationship(request, *args, **kwargs):
    priorURL = request.META.get('HTTP_REFERER')
    qs1 = Friend.objects.get(friend=User.objects.get(pk=kwargs['pk']), profile=request.user.userprofile)
    qs1.delete()
    qs2 = Friend.objects.get(friend=request.user, profile=User.objects.get(pk=kwargs['pk']))
    qs2.delete()
    url = reverse_lazy('forum:ajouter-amie')
    return redirect(priorURL)


# def AddAmie(request, *args, **kwargs):
#     priorURL = request.META.get('HTTP_REFERER')
#     user_cliquer = User.objects.get(id=kwargs['pk'])
#     id_user = request.user
#     print(user_cliquer.userprofile.friendlist)
#     print(type(user_cliquer))
#     print(id_user)
#     if user_cliquer in request.user.userprofile.friendlist:
#         request.user.userprofile.friendlist.remove(user_cliquer)
#         request.user.userprofile.save()
#     else:
#         request.user.userprofile.friendlist.add(user_cliquer)
#         request.user.userprofile.save()
#
#     return redirect(priorURL)


# QUESTION
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


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'question-create.html'
    fields = ['title', 'body', 'tags']

    def form_valid(self, form):

        # ici la logique de point
        if self.request.user.userprofile.point != 0:
            form.instance.user = self.request.user
            self.request.user.userprofile.point -= 1
            self.request.user.userprofile.save()
            messages.success(self.request, "Votre question a bien été envoyé")
        else:
            messages.error(self.request, "Votre question n'a pas pu être envoyée, votre fomulaire n'est pas bon")
        return super().form_valid(form)


class QuestionListView(ListView):
    paginate_by = 5
    model = Question
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        dateFormat = Question.created_at
        return context


class QuestionUpdateView(UpdateView):
    model = Question
    template_name = "question_update.html"
    fields = ['title', 'body']
    success_url = reverse_lazy('forum:forum-question')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "question_delete.html"

    def get_success_url(self):
        url = reverse_lazy('forum:forum-question')
        return redirect(url)


# nous avons deux vue qui nous permettent de défenir si c 'est une question ou une réponse
# donc deux url et relatif
# pour les question reverse d'url dans la template avec l'id de la question
# et la meme chose pour les reponse


def ChangeVoteQuestion(request, *args, **kwargs):
    priorURL = request.META.get('HTTP_REFERER')
    question = Question.objects.get(id=kwargs['pk'])
    toi = request.user

    if toi == question.user:
        # rajouter le message comm quoi on ne peut pas voté sa propre question
        return redirect(priorURL)
    if toi in question.questionvote.profile.all():
        question.questionvote.profile.remove(toi)
        request.user.userprofile.point -= 1
        request.user.userprofile.save()
    else:
        question.questionvote.profile.add(toi)
        request.user.userprofile.point += 1
        request.user.userprofile.save()
        return redirect(priorURL)
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
        answer.user.userprofile.point -= 1
        answer.user.userprofile.save()
    else:
        answer.answervote.profile.add(toi)
        answer.user.userprofile.point += 1
        answer.user.userprofile.save()
    return redirect(priorURL)


class FollowingListOfUser(DetailView):
    model = Profile
    template_name = 'following.html'


class FollowerListOfUser(DetailView):
    model = Profile
    template_name = 'follower.html'  # object.follower.all, object.following.all dans template in for loop


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
        return JsonResponse({'data': 'true'})
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


class TagView(ListAPIView):
    model = Question
    template_name = 'tag_list.html'
    queryset = Question.objects.all()
    serializer_class = TagFilterSlugModelSerializer
    lookup_field = 'slug'
    def get_queryset(self):
        return Question.objects.filter(tags__slug=self.kwargs.get('slug'))

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
        form = TagForm(request.POST or None)
        form.save()
        return render(request, 'landing.html', context={"form": form})

def Logout(request):
    logout(request)
    return redirect('forum:login')


# pour référence
def QuestionCreateSurMesure(request, *args, **kwarg):
    piorURL = request.META.HTTP_REFERER
    context = {}
    context['form'] = QuestionForm()
    if request.user.userprofile.points != 0:
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            form.save()
            request.user.userprofile.points -= 1
            request.user.userprofile.save()
            messages.success(request, "Votre question a bien été envoyé")
            return redirect('forum:forum-question')
        else:
            messages.error(request, "Votre question n'a pas pu être envoyée, votre fomulaire n'est pas bon")
            return render(request, '.html', context)
    else:
        messages.error(request, "Votre nombre de points est insuffisant")
        return render(request, '.html', context)


def CreateSurMesure(request, *args, **kwarg):
    priorURL = request.meta.HTTP_REFERER
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect(priorURL)
