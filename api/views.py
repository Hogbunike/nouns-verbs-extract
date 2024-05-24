from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import PDFDataSerializer
from .models import PDFData
from pdfminer.high_level import extract_text
from io import BytesIO
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

# Create your views here.


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


class PDFUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'email' not in request.data:
            return Response({"error": "No Email provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        email = request.data['email']

        file_content = BytesIO(file.read())
        content = extract_text(file_content)

        tokens = word_tokenize(content)
        tagged = pos_tag(tokens)

        nouns = [word for word, pos in tagged if pos.startswith('NN')]
        verbs = [word for word, pos in tagged if pos.startswith('VB')]


        data = {
            'email': email,
            'content': content,
            'nouns': ','.join(nouns),
            'verbs': ','.join(verbs)
        }
        serializer = PDFDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class PDFUploadFormView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'upload.html')