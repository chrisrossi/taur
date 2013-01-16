from pyramid.view import view_config
from pyramid.view import view_defaults

from .sites import Sites


@view_defaults(context=Sites)
class AdminUI(object):

    def __init__(self, context, request):
        self.sites = context
        self.request = request

    @view_config(renderer='templates/admin_home.pt')
    def home(self):
        return {'sites': sorted(self.sites.keys())}
