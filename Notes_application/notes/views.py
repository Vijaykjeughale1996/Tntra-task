from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Note, Image, NoteShare
from .serializers import NoteSerializer, CustomUserSerializer, NoteShareSerializer, ImageSerializer
# Create your views here.

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        #print(serializer)
        if serializer.is_valid():  # Validate the serializer first

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteCreateView(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteUpdateView(APIView):

    def put(self, request, note_id):
        note = Note.objects.get(pk=note_id)
        self.check_object_permissions(request, note)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = Note.objects.get(pk=note_id)
        self.check_object_permissions(request, note)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ImageCreateView(APIView):
    def post(self, request, note_id):
        note = Note.objects.get(pk=note_id)
        self.check_object_permissions(request, note)

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(note=note)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDeleteView(APIView):
    def delete(self, request, note_id, image_id):
        note = Note.objects.get(pk=note_id)
        self.check_object_permissions(request, note)
        
        try:
            image = Image.objects.get(pk=image_id, note=note)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        
class NoteShareView(APIView):

    def post(self, request, note_id):
        note = Note.objects.get(pk=note_id)
        self.check_object_permissions(request, note)

        if note.shared_with.count() >= 5:
            return Response({"error": "You cannot share this note with more than 5 members."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NoteShareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(note=note)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)