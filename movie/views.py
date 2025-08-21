from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    # return render(request, 'home.html', {'name':'Sebastián Rave'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies, 'name':'Sebastián Rave'})


def about(request):
    return render(request, 'about.html')


def statistics_page_view(request):
    matplotlib.use('Agg')

    all_movies = Movie.objects.all()

    # -------- Películas por año --------
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    plt.figure(figsize=(10, 5))
    positions_year = range(len(movie_counts_by_year))
    plt.bar(positions_year, movie_counts_by_year.values(), width=0.5)
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(positions_year, movie_counts_by_year.keys(), rotation=90)
    plt.tight_layout()

    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    graphic1_base64 = base64.b64encode(buffer1.getvalue()).decode()
    plt.clf()

    # -------- Películas por primer género (desde texto) --------
    movie_counts_by_genre = {}
    for movie in all_movies:
        genre_text = movie.genre.strip() if movie.genre else "None"
        # Tomar solo el primer género
        first_genre = genre_text.split(",")[0].strip() if genre_text != "None" else "None"
        movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    positions_genre = range(len(movie_counts_by_genre))
    plt.figure(figsize=(10, 5))
    plt.bar(positions_genre, movie_counts_by_genre.values(), width=0.5, color='orange')
    plt.title('Movies per Genre (First Genre Only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.tight_layout()

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    graphic2_base64 = base64.b64encode(buffer2.getvalue()).decode()

    return render(request, 'statistics.html', {
        'graphic': graphic1_base64,
        'graphic2': graphic2_base64
    })

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})