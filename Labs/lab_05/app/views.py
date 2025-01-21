import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from app.forms import LoginForm, RegisterForm, SettingsForm, AskForm, AnswerForm
from app.models import Question, Answer, Profile, Tag, User

# Список вопросов
QUESTIONS = [
    {
        'title': f'title{i}',
        'id': i,
        'text': f'This is text for QUESTIONS{i}',
    } for i in range(1, 30)
]

COLORS = [
    "text-bg-primary",
    "text-bg-secondary",
    "text-bg-success",
    "text-bg-danger",
    "text-bg-warning",
    "text-bg-info",
    "text-bg-dark",
]

TAGS = ['python', 'django', 'cpp', 'ml', 'probabylity', 'harrypotter', 'gym', 'elbobre', 'muertaporlalibertat']

def generate_colored_tags(tags, colors):
    return [{'tag': tag, 'color': colors[i % len(colors)]} for i, tag in enumerate(tags)]




def paginate(objects_list, request, per_page=5):
    try:
        page_number = request.GET.get('page', 1)
        paginator = Paginator(objects_list, per_page)

        page = paginator.page(page_number)
        return page

    except PageNotAnInteger:
        # Если номер страницы не число, возвращаем первую страницу
        return paginator.page(1)

    except EmptyPage:
        # Если номер страницы выходит за пределы, возвращаем последнюю доступную страницу
        return paginator.page(paginator.num_pages)

    except Exception as e:
        # Отлавливаем любое другое исключение
        print(f"Unexpected error during pagination: {e}")
        return None


def index(request):
    newQuestions = Question.objects.get_new()
    tags = Tag.objects.get_popular()
    page = paginate(newQuestions, request, per_page=3)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})
    
    color_tags = generate_colored_tags(tags, COLORS)

    return render(
        request,
        'index.html',
        context={
            'questions': page.object_list,
            'page_obj': page,
            'user': request.user, 
            'tags': tags,
            'color_tags': color_tags,
        }
    )


def hot_questions(request):
    hotQuestions = Question.objects.get_hot()
    tags = Tag.objects.get_popular()
    color_tags = generate_colored_tags(tags, COLORS)

    page = paginate(hotQuestions, request, per_page=5)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})

    return render(request, 'hotQuestions.html',
                  context={
                        'questions': page.object_list,
                        'page_obj': page,
                        'user': request.user, 
                        'tags': tags,
                        'color_tags': color_tags,
                    }
                )


def question(request, question_id):
    try:
        oneQuestion = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return render(request, 'error.html', context={'error': 'Вопрос не найден.'})
    
    answers = Answer.objects.get_answers_by_question_id(question_id)
    answerForm = AnswerForm()
    tags = Tag.objects.get_popular()
    color_tags = generate_colored_tags(tags, COLORS)

    if request.method == "POST":
        answerForm = AnswerForm(request.POST)
        if answerForm.is_valid():
            try:
                existing_answer = Answer.objects.get_answers_by_question_id(question_id).filter(
                    description=answerForm.cleaned_data['answer']
                ).first()
                if not existing_answer:
                    new_answer = answerForm.save(request.user, oneQuestion)
                    
                    # TODO переделать логику -> Идея :
                    # Сохранить ответ -> найти по id вопроса все ответы к нему
                    # пройтись по всем ответам (по страницам).Найти сохраненный ответ с 
                    # записанным в указанной странице. Переключить пользователя на страницу с ответом
                    paginator = Paginator(answers, 2) 
                    for page_number in range(1, paginator.num_pages + 1):
                        if new_answer in paginator.page(page_number).object_list:
                            return redirect(f"/question/{question_id}?page={page_number}#{new_answer.id}")
            except Exception as e:
                print(f"Answer creation error: {e}")
    
    page = paginate(answers, request, per_page=2)
    return render(request, 'pageQuestion.html', {
        'question': oneQuestion,
        'answers': page.object_list,
        'page_obj': page, 
        'answerForm': answerForm,  
        'tags': tags,
        'color_tags': color_tags,
    })

def tag(request, nameTag):
    questionByTag = Question.objects.get_by_tag(nameTag)
    tags = Tag.objects.get_popular()
    color_tags = generate_colored_tags(tags, COLORS)
    
    page = paginate(questionByTag, request, per_page=3)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})
    
    return render(
        request,
        'listing.html',
        context={
            'questions': page.object_list, 
            'page_obj': page, 
            "nameTag": nameTag, 
            'tags': tags,
            'color_tags': color_tags,
        }
    )


@login_required
def add_question(request):
    askForm = AskForm()
    tags = Tag.objects.get_popular()
    color_tags = generate_colored_tags(tags, COLORS)

    if request.method == "POST":
        askForm = AskForm(request.POST)
        if askForm.is_valid():
            try:
                questionId = askForm.save(request.user)
                return redirect(f"/question/{questionId}")
            except Exception as e:
                print(f"Question creation error: {e}")
                    
    return render(request, 'addQuestion.html', {
        'askForm': askForm, 
        'tags': tags,
        'color_tags': color_tags,
    })

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    registerForm = RegisterForm()
    
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        
        if registerForm.is_valid():
            if User.objects.filter(username=registerForm.cleaned_data.get("username")).exists():
                registerForm.add_error("username", "This username is already exists")
            else:
                newUser = registerForm.save()
                auth.login(request, newUser)
                return redirect("index") 
        else:
            registerForm.add_error(None, "Something went wrong! Try again")

        
            
    return render(request, 'register.html', {'registerForm': registerForm})

@login_required(redirect_field_name='continue')
def settings(request):
    settingsForm = SettingsForm()
    if request.user.is_authenticated:
        settingsForm = SettingsForm(initial=model_to_dict(request.user))

        if request.method == "POST":
            settingsForm = SettingsForm(request.POST, request.FILES)

            print("FORM files:", settingsForm.files)
            
            if settingsForm.is_valid():
                print("cleaned form:", settingsForm.cleaned_data)
                try:
                    settingsForm.save(request.user.id)
                except Exception as ex:
                    print(f"Update error: {ex}")
    
    return render(request, 'settings.html', {'settingsForm': settingsForm})


def log_in(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get("next", reverse("continue")))  

    loginForm = LoginForm()

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = auth.authenticate(request, **loginForm.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.POST.get("next", "/")) 
        else:
            loginForm.add_error(field="password", error="Wrong password!")

    return render(request, "login.html", {
        "loginForm": loginForm, 
        "next": request.GET.get("next", "/"),  
    })
    
    
def logout(request):
    print("inFunc")
    auth.logout(request)
    return redirect(reverse('index'))

@login_required(redirect_field_name="continue")
def like(request):
    
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
    
    
@login_required(redirect_field_name="continue")
def dislike(request):
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


