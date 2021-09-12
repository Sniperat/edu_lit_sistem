from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from .forms import LoginForm


class UserLoginView(View):
    """ User Login """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = LoginForm()
        context = {'form': form}
        print('asdasdasdasd')
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'],
                                backend='django.contrib.auth.backends.ModelBackend')
            print(user)
            if user is not None:
                login(request, user)
                if 'after-login' in request.session.keys():
                    return redirect(request.session['after-login'])
                if 'back-trans' in request.session.keys():
                    return redirect(request.session['back-trans'])

                return redirect('index')
            else:
                messages.error(request, 'Email or Password is invalid')
                context = {'form': form}
                return render(request, 'login.html', context)
