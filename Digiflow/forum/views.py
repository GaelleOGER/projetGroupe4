from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .forms import UserRegistrationForm, UserLoginForm, TagForm
from .models import Question, Tag


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




