from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from app.forms import LoginForm, RegisterForm, SettingsForm, AskForm, AnswerForm
from app.models import Question, Answer, Profile, Tag, User


def add_context(context: dict) -> None:
    top_tags = cache.get('top_tags')
    if top_tags is None:
        top_tags = Tag.objects.get_popular()

    top_members = cache.get('top_users')
    if top_members is None:
        top_members = Profile.objects.get_top_users()

    context["tags"] = top_tags
    context["members"] = top_members


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
    page = paginate(newQuestions, request, per_page=3)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})

    context = {
        'questions': page.object_list,
        'page_obj': page,
        'user': request.user,
        'color_tags': generate_colored_tags(Tag.objects.get_popular(), COLORS),
    }
    add_context(context)

    return render(request, 'index.html', context)


def hot_questions(request):
    hotQuestions = Question.objects.get_hot()
    page = paginate(hotQuestions, request, per_page=5)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})

    context = {
        'questions': page.object_list,
        'page_obj': page,
        'user': request.user,
        'color_tags': generate_colored_tags(Tag.objects.get_popular(), COLORS),
    }
    add_context(context)

    return render(request, 'hotQuestions.html', context)


def question(request, question_id):
    if request.user.is_authenticated:
        return redirect(request.GET.get("next", reverse("continue")))
    try:
        oneQuestion = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return render(request, 'error.html', context={'error': 'Вопрос не найден.'})

    answers = Answer.objects.get_answers_by_question_id(question_id)
    answerForm = AnswerForm()

    if request.method == "POST":
        answerForm = AnswerForm(request.POST)
        if answerForm.is_valid():
            try:
                existing_answer = Answer.objects.get_answers_by_question_id(question_id).filter(
                    description=answerForm.cleaned_data['answer']
                ).first()
                if not existing_answer:
                    new_answer = answerForm.save(request.user, oneQuestion)

                    paginator = Paginator(answers, 2)
                    for page_number in range(1, paginator.num_pages + 1):
                        if new_answer in paginator.page(page_number).object_list:
                            return redirect(f"/question/{question_id}?page={page_number}#{new_answer.id}")
            
            except Exception as e:
                print(f"Answer creation error: {e}")

    page = paginate(answers, request, per_page=2)
    context = {
        'question': oneQuestion,
        'answers': page.object_list,
        'page_obj': page,
        'answerForm': answerForm,
        'color_tags': generate_colored_tags(Tag.objects.get_popular(), COLORS),
        "next": request.GET.get("next", "/"),
    }
    add_context(context)

    return render(request, 'pageQuestion.html', context)


def tag(request, nameTag):
    questionByTag = Question.objects.get_by_tag(nameTag)
    page = paginate(questionByTag, request, per_page=3)
    if page is None:
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})

    context = {
        'questions': page.object_list,
        'page_obj': page,
        "nameTag": nameTag,
        'color_tags': generate_colored_tags(Tag.objects.get_popular(), COLORS),
    }
    add_context(context)

    return render(request, 'listing.html', context)

@login_required
def add_question(request):
    askForm = AskForm()

    if request.method == "POST":
        askForm = AskForm(request.POST)
        if askForm.is_valid():
            try:
                questionId = askForm.save(request.user)
                return redirect(f"/question/{questionId}")
            except Exception as e:
                print(f"Question creation error: {e}")

    context = {
        'askForm': askForm,
        'color_tags': generate_colored_tags(Tag.objects.get_popular(), COLORS),
    }
    add_context(context)

    return render(request, 'addQuestion.html', context)


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

    context = {'registerForm': registerForm}
    add_context(context)

    return render(request, 'register.html', context)


@login_required(redirect_field_name='continue')
def settings(request):
    settingsForm = SettingsForm()
    if request.user.is_authenticated:
        settingsForm = SettingsForm(initial=model_to_dict(request.user))

        if request.method == "POST":
            settingsForm = SettingsForm(request.POST, request.FILES)

            if settingsForm.is_valid():
                try:
                    settingsForm.save(request.user.id)
                except Exception as ex:
                    print(f"Update error: {ex}")

    context = {'settingsForm': settingsForm}
    add_context(context)

    return render(request, 'settings.html', context)


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

    context = {
        "loginForm": loginForm,
        "next": request.GET.get("next", "/"),
    }
    add_context(context)

    return render(request, "login.html", context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


@login_required(redirect_field_name="continue")
def like(request):
    if request.method == "POST":
        content_type = request.POST.get("content")
        content_id = request.POST.get("id")

        if content_id is not None:
            if content_type == "q":
                amount = Question.objects.add_like(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})

            elif content_type == "a":
                amount = Answer.objects.add_like(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})

        return JsonResponse({"amount": 0})

    return JsonResponse({"amount": 0})


@login_required(redirect_field_name="continue")
def dislike(request):
    if request.method == "POST":
        content_type = request.POST.get("content")
        content_id = request.POST.get("id")

        if content_id is not None:
            if content_type == "q":
                amount = Question.objects.add_dislike(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})

            elif content_type == "a":
                amount = Answer.objects.add_dislike(request.user.profile.id, content_id)
                return JsonResponse({"amount": amount})

        return JsonResponse({"amount": 0})

    return JsonResponse({"amount": 0})
