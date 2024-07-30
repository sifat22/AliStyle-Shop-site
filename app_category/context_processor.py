from .models import Category


def menu_links(request):
    all_cat = Category.objects.all()
    links = Category.objects.all().filter(is_popular = True)[:3]
    return dict(links = links,all_cat = all_cat)