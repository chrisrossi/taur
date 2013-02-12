from pyramid_layout.layout import layout_config


@layout_config(template="templates/admin_layout.pt")
class Layout(object):
    page_title = "Taur"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.js_url = request.static_url('taur:static/js/')

    def static(self, path):
        return self.request.static_url('taur:static/' + path)
