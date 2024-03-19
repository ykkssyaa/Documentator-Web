from django.shortcuts import render
from django.views.generic import DetailView

from .models import *


class DocumentPage(DetailView):
    model = Document
    slug_url_kwarg = 'number'
    slug_field = 'number'
    template_name = 'documents/document.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super(DocumentPage, self).get_context_data(**kwargs)
        context['title'] = 'Договор #' + self.object.number
        return context
