from django.urls import path
import documents.views as views

urlpatterns = [
    path('delete_all', views.delete_all_documents, name='delete_all'),
    path('duty/<int:duty_id>/update/', views.DutyUpdateView.as_view(), name='update_duty'),
    path('notifications', views.NotificationsListView.as_view(), name='notifications'),
    path('', views.DocumentListView.as_view(), name='list'),
    path('create', views.DocumentCreateView.as_view(), name='create'),
    path('<str:number>', (views.DocumentPage.as_view()), name='document'),
    path('<str:number>/update', (views.DocumentUpdateView.as_view()), name='update'),
    path('<int:pk>/delete', (views.DocumentDeleteView.as_view()), name='delete'),
]
