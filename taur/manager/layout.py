from pyramid_layout.layout import layout_config

from .application import Sites


@layout_config(context=Sites, template="templates/admin_layout.pt")
class AdminLayout(object):
    page_title = "Taur"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.js_url = request.static_url('taur:js/')

    def static(self, path):
        return self.request.static_url('taur.manager:static/' + path)

    def js(self, path):
        return self.request.static_url('taur:js/' + path)
