from pyramid.view import view_config

from .models import Site


@view_config(context=Site, renderer='templates/home_page.pt')
def home_page(context, request):
    return {}
