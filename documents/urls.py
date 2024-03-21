from django.contrib.auth.decorators import login_required
from django.urls import path
import documents.views as views

urlpatterns = [
    path('notifications', login_required(views.NotificationsListView.as_view()), name='notifications'),
    path('', login_required(views.DocumentListView.as_view()), name='list'),
    path('create', login_required(views.DocumentCreateView.as_view()), name='create'),
    path('<str:number>', login_required(views.DocumentPage.as_view()), name='document'),
    path('<str:number>/update', login_required(views.DocumentUpdateView.as_view()), name='update'),
    path('<int:pk>/delete', login_required(views.DocumentDeleteView.as_view()), name='delete'),
]
