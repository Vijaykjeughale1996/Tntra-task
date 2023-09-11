from django.urls import path
from .views import UserRegistrationView, NoteCreateView, NoteUpdateView, NoteShareView, ImageCreateView, ImageDeleteView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('notes/create/', NoteCreateView.as_view(), name='note-create'),
    path('notes/<int:note_id>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:note_id>/images/', ImageCreateView.as_view(), name='image-create'),
    path('notes/<int:note_id>/images/<int:image_id>/', ImageDeleteView.as_view(), name='image-delete'),
    path('notes/<int:note_id>/share/', NoteShareView.as_view(), name='note-share'),
]