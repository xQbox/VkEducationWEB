import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from app.models import Question, Answer, Profile, Tag

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
        return render(request, 'error.html', context={'error': 'Ошибка при обработке пагинации.'})

    return render(request, 'pageQuestion.html',
                  context={'question': oneQuestion}
                  )


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


def add_question(request):
    return render(request, 'addQuestion.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')


def log_in(request):
    return render(request, 'login.html')
