from re import M
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import is_valid_path

from .models import Movie,Comment


from django.views.generic import ListView

from django.views.decorators.http import require_POST

from .forms import EmailSharePost,CommentForm

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from django.core.mail import send_mail





class IndexHome(ListView):

    queryset = Movie.published.all()

    template_name = 'mov/movie/index.html'

    context_object_name = 'movies'



def detail_movie(request,year,month,day,movie):

    movie = get_object_or_404(Movie,
                              status=Movie.Status.PUBLISHED,
                              publish__year=year,
                              publish__month=month,
                              publish__day=day,
                              slug=movie)
    
    comments = movie.comments.filter(active=True)

    form = CommentForm()

    return render(request,'mov/movie/detail.html',{'details':movie,
                                                   'comments':comments,
                                                   'form':form})




def share_movie(request,movie_id):

    movie = get_object_or_404(Movie,
                              id=movie_id,
                              status=Movie.Status.PUBLISHED)
    
    sent = False
    
    if request.method=='POST':
        
        form_share = EmailSharePost(request.POST)

        if form_share.is_valid():
            
            cd = form_share.cleaned_data

            movie_url = request.build_absolue_uri(movie.get_absolute_url())

            subject = f"{cd['name']} recommends watching a {movie.title}"

            message = f"Watch the {movie.title} at the {movie_url}\n\n"
            f"Commentary {cd['name']} for the film {movie.title}: {cd['comment']}"

            send_mail(subject,
                      message,
                      'kaznacheev724@gmail.com',
                      [cd['to']])
            
            sent = True

    else:
        form_share = EmailSharePost()

    return render(request,'mov/movie/share.html',{'form':form_share,
                                                  'sent':sent,
                                                  'movie':movie})







@require_POST
def movie_comment(request,movie_id):

    movie = get_object_or_404(Movie,
                              id=movie_id,
                              status = Movie.Status.PUBLISHED)
    
    comment = None

    form_comment = CommentForm(data=request.POST)

    if form_comment.is_valid():

        comment = form_comment.save(commit=False)

        comment.movie = movie

        comment.save()

    return render(request,'mov/movie/comment.html',{'movie':movie,
                                                    'comment':comment,
                                                    'form':form_comment})



