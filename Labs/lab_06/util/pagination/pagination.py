from django.core.paginator import Paginator


def paginate(request, objects, per_page=2):
    page_number = request.GET.get("page")

    if page_number == None:
        page_number = 1

    paginator = Paginator(objects, per_page)
    return paginator.page(page_number)
