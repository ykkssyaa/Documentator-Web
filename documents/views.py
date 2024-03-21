from django.http import Http404
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, ListView

from .forms import DocumentForm
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


class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/add_document.html'
    extra_context = {
        'title': 'Создание договора',
    }

    def get_success_url(self):
        return reverse('documents:document', kwargs={'number': self.object.number})


class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/add_document.html'
    extra_context = {
        'title': 'Изменение договора',
    }
    slug_url_kwarg = 'number'
    slug_field = 'number'

    def get_initial(self):
        initial = super().get_initial()
        duties = self.object.duty_set.values_list('title', flat=True)
        initial['duties'] = '\n'.join(duties)
        initial['signing_date'] = self.object.signing_date.strftime('%Y-%m-%d') if self.object.signing_date else ''
        initial['end_date'] = self.object.end_date.strftime('%Y-%m-%d') if self.object.end_date else ''
        return initial

    def get_success_url(self):
        return reverse('documents:document', kwargs={'number': self.object.number})


class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context['title'] = 'Список договоров'

        edit_arg = self.request.GET.get('edit')
        if edit_arg:
            context['title'] = 'Редактирование договоров'
            context['edit'] = 1

        return context


class DocumentDeleteView(View):
    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)

        # Получаем значение параметра next из запроса, если оно есть
        next_url = request.GET.get('next', reverse_lazy('documents:list'))

        # Удаляем документ
        document.delete()

        # Перенаправляем пользователя на указанную страницу
        return redirect(next_url)


class NotificationsListView(ListView):
    model = Document
    template_name = 'documents/notifications.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        context = super(NotificationsListView, self).get_context_data(**kwargs)
        context['title'] = 'Уведомления'

        return context

    def get_queryset(self):
        # Получаем текущую дату
        current_date = timezone.now()

        # Вычисляем дату, за неделю до текущей даты
        week_from_now = current_date + timezone.timedelta(days=7)

        # Фильтруем документы, у которых end_date находится в пределах недели от текущей даты
        queryset = Document.objects.filter(end_date__lte=week_from_now, status__in=['В обработке', 'Подписан', 'В исполнении'])

        # Для каждого документа вычисляем количество дней до конца договора
        for document in queryset:
            remaining_days = (document.end_date - current_date).days
            document.remaining_days = remaining_days

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Если список пуст, просто возвращаем пустой queryset
            return Document.objects.none()
