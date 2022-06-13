# import logging

from django.shortcuts import render
from ..models import Movie, Actor, MovieActor, Director, MovieDirector, \
                    Image, Video, Jenre, Nation, Point, Review, MovieReview, Review2
from django.core.paginator import Paginator  
from django.db.models import Q

# logger = logging.getLogger('pybo')

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    akw = request.GET.get('akw', '') # 배우 검색어
    dkw = request.GET.get('dkw', '') # 감독 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'audience_rate':
        movie_list = Movie.objects.order_by('-audience_rate')
    elif so == 'journalist_rate':
        movie_list = Movie.objects.order_by('-journalist_rate')
    elif so == 'netizen_rate':
        movie_list = Movie.objects.order_by('-netizen_rate')
    elif so == 'title':
        movie_list = Movie.objects.order_by('title')
    else:  # 이름순
        movie_list = Movie.objects.order_by('-opening_date')

    # 검색
    if kw:
        movie_list = movie_list.filter(
            Q(title__icontains=kw) |
            Q(original_title__icontains=kw) |
            Q(content__icontains=kw) |
            Q(subtitle__icontains=kw)
        ).distinct()
    
    if akw:
        actors = Actor.objects.filter(Q(actor_name__icontains=akw)).values('actor_code')
        movie_codes = MovieActor.objects.filter(actor_code__in=actors).values('movie_code')
        movie_list = movie_list.filter(
            movie_code__in=movie_codes
        ).distinct()
    
    if dkw:
        directors = Director.objects.filter(Q(director_name__icontains=dkw)).values('director_code')
        movie_codes2 = MovieDirector.objects.filter(director_code__in=directors).values('movie_code')
        movie_list = movie_list.filter(
            movie_code__in=movie_codes2
        ).distinct()
        
    paginator = Paginator(movie_list, 20)  # 페이지당 20개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'movie_list': page_obj, 'page':page, 'kw':kw, 'so':so, 'akw':akw, 'dkw':dkw}
    # context = {'movie_list': page_obj}
    return render(request, 'pybo/movie_list.html', context)
def detail(request, movie_code):
    movie = Movie.objects.get(movie_code=movie_code)
    jenre = Jenre.objects.filter(movie_code=movie_code)
    nation = Nation.objects.filter(movie_code=movie_code)
    movie_actor = MovieActor.objects.filter(movie_code=movie_code)
    movie_director = MovieDirector.objects.filter(movie_code=movie_code)
    movie_review = MovieReview.objects.filter(movie_code=movie_code)
    image  = Image.objects.filter(movie_code=movie_code)
    video  = Video.objects.filter(movie_code=movie_code)
    point = Point.objects.filter(movie_code=movie_code)
    context = {'movie': movie, 'jenre': jenre, 'nation': nation, 'movie_actor':movie_actor, 'movie_director':movie_director, 'movie_review':movie_review, 'image': image, 'video': video, 'point':point}
    return render(request, 'pybo/movie_detail.html', context)
def review(request, review_code):
    review = Review.objects.get(review_code=review_code)
    review2 = Review2.objects.filter(review_code=review_code)
    context = {'review':review, 'review2':review2}
    return render(request, 'pybo/movie_review.html', context)
