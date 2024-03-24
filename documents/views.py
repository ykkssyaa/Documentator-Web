from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, ListView

from .forms import DocumentForm
from .models import *


class DocumentPage(LoginRequiredMixin, DetailView):
    model = Document
    slug_url_kwarg = 'number'
    slug_field = 'number'
    template_name = 'documents/document.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super(DocumentPage, self).get_context_data(**kwargs)
        context['title'] = 'Договор #' + self.object.number
        return context


class DocumentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/add_document.html'
    extra_context = {
        'title': 'Создание договора',
    }
    permission_required = 'documents.add_document'

    def get_success_url(self):
        return reverse('documents:document', kwargs={'number': self.object.number})


class DocumentUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/add_document.html'
    extra_context = {
        'title': 'Изменение договора',
    }
    slug_url_kwarg = 'number'
    slug_field = 'number'
    permission_required = 'documents.change_document'

    def get_initial(self):
        initial = super().get_initial()
        duties = self.object.duty_set.values_list('title', flat=True)
        initial['duties'] = '\n'.join(duties)
        initial['signing_date'] = self.object.signing_date.strftime('%Y-%m-%d') if self.object.signing_date else ''
        initial['end_date'] = self.object.end_date.strftime('%Y-%m-%d') if self.object.end_date else ''
        return initial

    def get_success_url(self):
        return reverse('documents:document', kwargs={'number': self.object.number})


class DocumentListView(LoginRequiredMixin, ListView):
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


class DocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = 'documents.delete_document'

    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)

        # Получаем значение параметра next из запроса, если оно есть
        next_url = request.GET.get('next', reverse_lazy('documents:list'))

        # Удаляем документ
        document.delete()

        # Перенаправляем пользователя на указанную страницу
        return redirect(next_url)


class NotificationsListView(LoginRequiredMixin, ListView):
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


class DutyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'documents.change_duty'

    def post(self, request, duty_id, *args, **kwargs):
        # Получаем объект обязательства (Duty) по его идентификатору
        duty = Duty.objects.get(pk=duty_id)

        # Проверяем, что запрос содержит значение done
        if 'done' in request.POST:
            # Обновляем значение done
            duty.done = request.POST['done'] == 'true'  # Преобразуем строку 'true' в булево значение True

            # Сохраняем изменения в базе данных
            duty.save()

            # Возвращаем JSON-ответ, чтобы обновить представление на стороне клиента
            return JsonResponse({'success': True})

        # Если значение done отсутствует в запросе, возвращаем ошибку
        return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
@permission_required('documents.delete_document')
def delete_all_documents(request):
    if request.method == 'POST':
        # Удаляем все документы
        Document.objects.all().delete()
        
    return redirect('users:settings')
