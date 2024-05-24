from django.urls import path
from .views import PDFUploadView, PDFUploadFormView

urlpatterns = [
    path('upload/', PDFUploadView.as_view(), name='pdf-upload'),
    path('upload-form/', PDFUploadFormView.as_view(), name='upload-form'),
]