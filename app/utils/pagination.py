from django.template.loader_tags import register


class Pagination():

    page = 1
    perPage = 20
    count = 0
    name = "page"
    url = None
    url_add = ""

    @property
    def ifrom(self):
        return (self.page-1)*self.perPage

    @property
    def ito(self):
        return self.ifrom + self.perPage

    @property
    def pages_count(self):
        return self.count / self.perPage

    def page_prev(self):
        return self.page - 1

    def page_next(self):
        return self.page + 1

    def range(self):
        return range(1, self.pages_count+1)

    def __str__(self):
        return "Page "+str(self.page)+" of "+str(self.pages_count)