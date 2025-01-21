import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
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
    "text-bg-light",
    "text-bg-dark",
]


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
    page = paginate(newQuestions, request, per_page=5)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})

    return render(
        request,
        'index.html',
        context={
            'questions': page.object_list,
            'page_obj': page,
            'user': request.user, 
        }
    )


def hot_questions(request):
    hotQuestions = Question.objects.get_hot()
    page = paginate(hotQuestions, request, per_page=5)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})

    return render(request, 'hotQuestions.html',
                  context={'questions': page.object_list, 'page_obj': page}
                  )


def question(request, question_id):
    try:
        oneQuestion = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return render(request, 'error.html', context={'error': 'Вопрос не найден.'})
    
    answers = Answer.objects.get_answers_by_question_id(question_id)
    print(answers)
    answerForm = AnswerForm()

    if request.method == "POST":
        answerForm = AnswerForm(request.POST)
        if answerForm.is_valid():
            try:
                existing_answer = Answer.objects.get_answers_by_question_id(question_id).filter(
                    description=answerForm.cleaned_data['answer']
                ).first()
                if not existing_answer:
                    answerForm.save(request.user, oneQuestion)
            except Exception as e:
                print(f"Answer creation error: {e}")
    
    page = paginate(answers, request, per_page=2)
    if not page:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})
    
    return render(request, 'pageQuestion.html', {
        'question': oneQuestion,
        'answers': page.object_list,
        'page_obj': page, 
        'answerForm': answerForm,  
    })


def tag(request):
    questionByTag = Question.objects.get_by_tag(tag)
    page = paginate(questionByTag, request, per_page=5)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})
    return render(
        request,
        'listing.html',
        context={'questions': page.object_list, 'page_obj': page}
    )



@login_required(redirect_field_name="continue")
def add_question(request):
    askForm = AskForm()
    if request.user.is_authenticated:
        if request.method == "POST":
            askForm = AskForm(request.POST)
            if askForm.is_valid():
                try:
                    questionId = askForm.save(request.user)
                    return redirect(f"/question/{questionId}")
                    # return redirect(reverse('question', questionId))
                except Exception as e:
                    print(f"Question creation error: {e}")
                    
    return render(request, 'addQuestion.html', {'askForm': askForm})


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

@login_required
def settings(request):
    return render(request, 'settings.html')


def log_in(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))
    
    loginForm = LoginForm()

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = auth.authenticate(request, **loginForm.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.POST.get("continue", "index"))
        else:
            loginForm.add_error(field="password", error="Wrong password!")

    return render(request, "login.html", {"loginForm": loginForm})

def logout(request):
    print("inFunc")
    auth.logout(request)
    return redirect(reverse('index'))














































