from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .forms import UserRegistrationForm, UserLoginForm
from .models import Question


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


class UserLoginView(View):
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

class HomeView(ListView):
    model = Question
    template_name = "home.html"