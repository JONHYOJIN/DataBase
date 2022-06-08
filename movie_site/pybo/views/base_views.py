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
    # so = request.GET.get('so', 'title')  # 정렬기준

    movie_list = Movie.objects.order_by('title')
    # # 정렬
    # if so == 'audience_rate':
    #     movie_list = Movie.objects.order_by('audience_rate')
    # elif so == 'recent':
    #     movie_list = Movie.objects.order_by('-opening_date')
    # else:  # 이름순
    #     movie_list = Movie.objects.order_by('title')
    # 검색
    if kw:
        movie_list = movie_list.filter(
            Q(title__icontains=kw)
        ).distinct()
    paginator = Paginator(movie_list, 20)  # 페이지당 20개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'movie_list': page_obj, 'page':page, 'kw':kw}
    # context = {'movie_list': page_obj}
    return render(request, 'pybo/movie_list.html', context)
def detail(request, movie_code):
    movie = Movie.objects.get(movie_code=movie_code)
    jenre = Jenre.objects.filter(movie_code=movie_code)
    nation = Nation.objects.filter(movie_code=movie_code)
    movie_actor = MovieActor.objects.filter(movie_code=movie_code)
    movie_director = MovieDirector.objects.filter(movie_code=movie_code)
    image  = Image.objects.filter(movie_code=movie_code)
    video  = Video.objects.filter(movie_code=movie_code)
    point = Point.objects.filter(movie_code=movie_code)
    context = {'movie': movie, 'jenre': jenre, 'nation': nation, 'movie_actor':movie_actor, 'movie_director':movie_director, 'image': image, 'video': video, 'point':point}
    return render(request, 'pybo/movie_detail.html', context)
