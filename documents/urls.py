from django.urls import path
import documents.views as views

urlpatterns = [
    path('<str:number>', views.DocumentPage.as_view(), name='document'),
]
