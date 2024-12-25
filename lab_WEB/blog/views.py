from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from util.mock.mock import *
from util.pagination.pagination import paginate
from blog.forms import LoginForm, SignupForm, SettingsForm, AskForm, AnswerForm
from blog.models import Question, Answer, Profile, Tag, User


def add_context(context: dict) -> None:
    top_tags = cache.get('top_tags')
    if top_tags == None:
        top_tags = Tag.objects.get_popular()
    
    top_members = cache.get('top_users')
    if top_members == None:
        top_members = Profile.objects.get_top_users()
    
    context["tags"] = top_tags
    context["members"] = top_members


@csrf_protect
def new(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('index.html')
    questions = Question.objects.get_new()

    try:
        pages = paginate(request, questions)
    except Exception as ex:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    
    context = {
        "questions": pages,
        "title": "New Questions",
        "subtitle": "Hot Questions",
        # "name": "Saul Goodman"
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


@csrf_protect
def hot(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('index.html')
    questions = Question.objects.get_hot()

    try:
        pages = paginate(request, questions)
    except Exception:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    context = {
        "questions": pages, 
        "title": "Hot Questions",
        # "name": "Saul Goodman"
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


@csrf_protect
def tag(request: HttpRequest, tag: str) -> HttpResponse:
    template = loader.get_template('index.html')

    questions = Question.objects.get_by_tag(tag)

    title = f'Tag: {tag}'
    if questions.count() == 0:
        title = f"No questions with tag '{tag}'"

    try:
        pages = paginate(request, questions)
    except Exception:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    context = {
        "questions": pages,
        "title": title,
        # "name": "Saul Goodman"
    }
    add_context(context)
    
    return HttpResponse(
        template.render(
            context,
            request
        )
    )


@csrf_protect
def question(request: HttpRequest, id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("/")
    
    template = loader.get_template('answers.html')

    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    answers = Answer.objects.get_answers_by_question_id(id)

    answerForm = AnswerForm()

    if request.method == "POST":
        answerForm = AnswerForm(request.POST)
        if answerForm.is_valid():
            try:
                Answer.objects.get_answers_by_question_id(id).\
                    get(description=answerForm.cleaned_data['answer'])
            except Answer.DoesNotExist:
                try:
                    answer_id = answerForm.save(request.user, question)
                except Exception as ex:
                    print(f"Answer creation error: {ex}")

    try:
        pages = paginate(request, answers)
    except Exception as ex:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    context = {
        "question": question,
        "answers": pages,
        "title": f"Question {id}",
        "answer_form": AnswerForm(),
        "amount": len(answers),
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


@csrf_protect
def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("/")
    
    template = loader.get_template('login.html')
    login_form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.POST.get("continue", "/"))
        else:
            login_form.add_error(field="password", error="Wrong password")

    return HttpResponse(
        template.render(
            context={
                'login_form': login_form,
            },
            request=request
        )
    )


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect(reverse('login-page'))


@csrf_protect
def signup(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('signup.html')

    if request.user.is_authenticated:
        return redirect("/")

    signup_form = SignupForm()

    if request.method == "POST":
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            if User.objects.filter(username=signup_form.cleaned_data.get("username")).exists():
                signup_form.add_error("username", "Such account already exists")
            else:
                new_user = signup_form.save()
                auth.login(request, new_user)
                # return redirect(request.POST.get("continue", "/"))
                return redirect("/")
        else:
            print("NOT VALID")

    return HttpResponse(
        template.render(
            {'signup_form': signup_form,},
            request=request
        )
    )


@csrf_protect
@login_required(login_url="/login", redirect_field_name="continue")
def ask(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("/")
    
    template = loader.get_template('ask.html')
    ask_form = AskForm()

    if request.user.is_authenticated:
        if request.method == "POST":
            ask_form = AskForm(request.POST)
            if ask_form.is_valid():
                try:
                    question_id = ask_form.save(request.user)
                    return redirect(f"/question/{question_id}")
                except Exception as ex:
                    print(f"Question creation error: {ex}")

    context = {
        'ask_form': ask_form,
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


@csrf_protect
@login_required(login_url="/login", redirect_field_name="continue")
def settings(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('settings.html')
    settings_form = SettingsForm()

    if request.user.is_authenticated:
        settings_form = SettingsForm(initial=model_to_dict(request.user))

        if request.method == "POST":
            settings_form = SettingsForm(request.POST, request.FILES)

            print("FORM files:", settings_form.files)
            
            if settings_form.is_valid():
                print("cleaned form:", settings_form.cleaned_data)
                try:
                    settings_form.save(request.user.id)
                except Exception as ex:
                    print(f"Update error: {ex}")

    context = {'settings_form': settings_form}
    add_context(context)
    
    return HttpResponse(
        template.render(
            context,
            request
        )
    )


@csrf_protect
@login_required(login_url="/login", redirect_field_name="continue")
def like(request: HttpRequest) -> HttpResponse:
    # return JsonResponse({"hello": "world"})

    if request.method == "POST":
        content_type = request.POST.get("content")
        content_id = request.POST.get("id")

        if content_id != None:
            if content_type == "q":
                amount = Question.objects.add_like(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})

            elif content_type == "a":
                amount = Answer.objects.add_like(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})
            else:
                return JsonResponse({"amount": 0})
        else:
            return JsonResponse({"amount": 0})
        
    return JsonResponse({"amount": 0})


@csrf_protect
@login_required(login_url="/login", redirect_field_name="continue")
def dislike(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        content_type = request.POST.get("content")
        content_id = request.POST.get("id")

        if content_id != None:
            if content_type == "q":
                amount = Question.objects.add_dislike(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})

            elif content_type == "a":
                amount = Answer.objects.add_dislike(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})
            else:
                return JsonResponse({"amount": 0})
        else:
            return JsonResponse({"amount": 0})
        
    return JsonResponse({"amount": 0})


@csrf_protect
@login_required(login_url="/login", redirect_field_name="continue")
def status(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        answer_id = request.POST.get("answer_id")
        question_id = request.POST.get("question_id")

        if answer_id != None and question_id != None:
            status = Answer.objects.toggle_correct(request.user.profile.id, question_id, answer_id)
            return JsonResponse({"status": status})
        else:
            return JsonResponse({"status": False})
        
    return JsonResponse({"status": False})

