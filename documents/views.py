from django.shortcuts import render
from django.views.generic import DetailView

from .models import *


class DocumentPage(DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super(DocumentPage, self).get_context_data(**kwargs)
        context['title'] = 'Договор #' + self.object.number
        return context
