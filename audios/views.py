from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from authentication_app.decorators import admin_required
from cloudinary import CloudinaryResource



# Create your views here.


def index(request):
    logo = Logo.objects.all()
    buk_logo = bukMosque.objects.all()

    context = {
         'logo': logo,
         'buk_logos': buk_logo
    }
    return render(request, 'audios/index.html', context)


def speaker_list(request):
    shiekhs_list = Shiekh.objects.all()
    paginator = Paginator(shiekhs_list, 10) 

    page = request.GET.get('page')
    try:
        shiekhs = paginator.page(page)
    except PageNotAnInteger:
    
        shiekhs = paginator.page(1)
    except EmptyPage:

        shiekhs = paginator.page(paginator.num_pages)

    context =  {
        'shiekhs': shiekhs,
        }

    return render(request, 'audios/speaker_list.html', context)


def books_by_shiekh(request, slug_id):
    shiekh = get_object_or_404(Shiekh, id=slug_id)
    books = Book.objects.filter(shiekh=shiekh)

    context = {
        'shiekh': shiekh,
        'books':books
    }
    return render(request, 'audios/books_by_shiekh.html', context)



def episodes_by_book(request, episode_id):
    book = get_object_or_404(Book, id=episode_id)
    episodes = AudioEpisode.objects.filter(book=book)


    paginator = Paginator(episodes, 10)
    page = request.GET.get('page')

    try:
        episodes = paginator.page(page)
    except PageNotAnInteger:
        episodes =paginator.page(1)
    except EmptyPage:
        episodes = paginator.page(paginator.num_pages)

    context = {

        'book':book,
        'episodes':episodes
    }

    return render(request, 'audios/episodes_by_book.html', context)

def download_audio(request, episode_id):
    episode = get_object_or_404(AudioEpisode, id=episode_id)
    # audio_resource = CloudinaryResource(episode.audio_file)
    audio_url = episode.audio_file.url
    context = {
        'audio_url':audio_url,
    }

    return render(request, 'audios/download_audio.html', context)


def search_results(request):
    query = request.GET.get('query')
    if query:
        shiekhs = Shiekh.objects.filter(Q(name__icontains=query))
        books = Book.objects.filter(Q(title__icontains=query))
        episodes = AudioEpisode.objects.filter(Q(title__icontains=query))
    else:
        shiekhs = books = episodes = None
    context = {
        'query':query,
        'shiekhs': shiekhs,
        'books':books,
        'episodes':episodes,
    }

    return render(request, 'audios/search_results.html', context)



@login_required
@admin_required
def add_shiekh(request):
    if request.method == 'POST':
        shiekh_form = ShiekhForm(request.POST, request.FILES)
        if shiekh_form.is_valid():
            shiekh = shiekh_form.save(commit=False)
            shiekh.owner = request.user
            

            if 'image' in request.FILES:
                shiekh.image = request.FILES['image']
            
            shiekh.save()
            return redirect('audios:add_book')
    else:
        shiekh_form = ShiekhForm()
    
    context = {
        'shiekh_form': shiekh_form
        }

    return render(request, 'audios/add_sheikh.html', context)



@login_required
@admin_required
def add_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.save()
            return redirect('audios:select_audio', book_id=book.id)

    else:
        book_form = BookForm()
    
    context =  {'book_form': book_form}

    return render(request, 'audios/add_book.html', context)

@login_required
@admin_required
def select_audio(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    audio_form = AudioEpisodeForm()

    if request.method == 'POST':
        audio_form = AudioEpisodeForm(request.POST, request.FILES)
        if audio_form.is_valid():
            title = f"audio {AudioEpisode.objects.filter(book=book).count() + 1}"
            audio = audio_form.save(commit=False)
            
            
            similar_record = AudioEpisode.objects.filter(book=book, title=title).exists()
            if similar_record:
                boks = Book.objects.all()
                sheikhs = Shiekh.objects.all()
                context = {
                    'audio_form': audio_form,
                    'book': book,
                    'boks': boks,
                    'sheikhs': sheikhs,
                    'error_message': 'Record already exists for this book.'
                }
                return render(request, 'audios/add_records.html', context)

            audio.book = book
            audio.title = title
            audio.uploaded_by = request.user
            audio.save()
            return redirect('audios:select_audio', book_id=book_id)

    return render(request, 'audios/add_records.html', {'audio_form': audio_form, 'book': book})

