from .models import Brand


def menu_links_brand(request):
    links = Brand.objects.all()
    return dict(b_links = links)