from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegistrationForm


class UserRegistrationView(View):
    template_name = "user_registration_form.html"

    def get(self, request):
        context = {}
        context['form'] = UserRegistrationForm()
        # param1= request, parm2=template, param3=context
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

            return redirect('forum:')
