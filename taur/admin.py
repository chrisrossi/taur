from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults

from .models import Sites


@view_defaults(context=Sites)
class AdminUI(object):

    def __init__(self, context, request):
        self.sites = context
        self.request = request
        self.layout = self.request.layout_manager.layout

    @view_config(renderer='templates/admin_home.pt')
    def home(self):
        self.layout.page_title = "Taur: Manage Sites"
        return {
            'add_site_url': self.request.resource_url(self.sites, 'add_site'),
            'sites': self.sites.proxies()
        }

    @view_config(name="add_site")
    def add_site(self):
        title = self.request.params['title']
        assert title
        self.sites.create(title)
        return HTTPFound(self.request.application_url)
