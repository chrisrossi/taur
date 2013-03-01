import churro


class Page(churro.PersistentFolder):
    title = churro.PersistentProperty()
    body = churro.PersistentProperty()


class Site(Page):
    hostname = churro.PersistentProperty()
    settings = {}
