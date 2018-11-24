from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.http import Http404


def error(request):
    return render(request, 'Error.html')


def user_signup(request):
    if request.method == "GET":
        if check_session_cookie(request):
            session = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
            if check_token_ttl(session):
                messages.info(request, 'Your\'re already signed in!')
                return HttpResponseRedirect('/error')

        signup_form = UserSignUpForm()
        return render(request, 'userSignUp.html', {'form': signup_form})

    elif request.method == "POST":
        signup_form = UserSignUpForm(request.POST)

        if signup_form.is_valid():
            name = signup_form.cleaned_data["name"]
            email_id = signup_form.cleaned_data["email_address"]
            password = signup_form.cleaned_data["password"]
            dateOfBirth = signup_form.cleaned_data["dateOfBirth"]

            new_user = UserModel(name=name, email_address=email_id, dateOfBirth=dateOfBirth, password=make_password(password))
            new_user.save()

            messages.info(request, 'Successfully Signed Up, Please enter your details again to Log in')
            return HttpResponseRedirect('/')

        else:
            messages.error(request, 'Invalid Data Submitted')
            return HttpResponseRedirect('/')


def user_login(request):
    if request.method == "GET":
        if check_session_cookie(request):
            sessionVar = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()

            if check_token_ttl(sessionVar):
                messages.info(request, "You\'re already signed in!")
                return HttpResponseRedirect('/error')

        login_form = LogInForm()
        return render(request, 'userLogin.html', {'form': login_form})

    elif request.method == "POST":
        login_form = LogInForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data["email_address"]
            password = login_form.cleaned_data["password"]

            user_fromDB = UserModel.objects.filter(email_address=email).first()

            if user_fromDB:
                if check_password(password, user_fromDB.password):
                    session_token = UserSessionToken(user=user_fromDB)
                    session_token.create_token()
                    session_token.save()

                    request.session['session_token'] = session_token.session_token
                    response = redirect('/photos/feed')
                    return response
                else:
                    messages.error(request, 'Invalid Password, please try again')
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'No Registered User found with the given Email Address')
                return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Invalid Data Submitted in Log In Form')
            return HttpResponseRedirect('/')


def logout(request):
    if request.method == "GET":
        del request.session['session_token']
        request.session.modified = True
        return HttpResponseRedirect("/")
    else:
        raise Http404


def check_user_token_validation(request):
    if check_session_cookie(request):
        session = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()

        if check_token_ttl(session):
            return True
        else:
            messages.error(request, 'Your Session has expired, please log in again to continue')
            return HttpResponseRedirect('/')
    else:
        messages.info(request, 'Please Log in first to access the page')
        return HttpResponseRedirect('/')


def check_session_cookie(request):
    if request.session.get('session_token') is not None:
        return True
    else:
        return False


def check_token_ttl(token):
    time_to_live = token.created_on + timedelta(days=1)

    if time_to_live > timezone.now():
        return True
    else:
        token.delete()
        return False


def get_user(request):
    if check_session_cookie(request):
        sessionVar = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()

        if sessionVar is None:
            raise Http404

        if check_token_ttl(sessionVar):
            return sessionVar.user

    return None
