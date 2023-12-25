from django.urls import path, include

from . import views

app_name = 'audios'

urlpatterns = [
    path('', views.index, name='index'),
    path('audios/', views.index, name='index'),
    path('speakers_list/', views.speaker_list, name='speaker_list'),
    path('books/<slug:slug_id>/', views.books_by_shiekh, name='books_by_shiekh'),
    path('episodes/<int:episode_id>/', views.episodes_by_book, name='episodes_by_book'),
    path('download/<int:episode_id>/', views.download_audio, name='download_audio'),
    path('search_results/', views.search_results, name='search_results'),
    path('add_shiekh/', views.add_shiekh, name='add_shiekh'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_records/<int:book_id>/', views.select_audio, name='select_audio'),
]