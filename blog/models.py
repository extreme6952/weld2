from django.db import models

from django.db.models import QuerySet

from django.utils import timezone

from django.urls import reverse 




class PublishedManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Movie.Status.PUBLISHED)





    




class Movie(models.Model):

    class Status(models.TextChoices):

        DRAFT = 'DF','Draft'

        PUBLISHED = 'PB','Published'


    title = models.CharField(max_length=250,
                             unique=True)
    
    slug = models.SlugField(max_length=250,unique=True)
    
    image = models.ImageField(upload_to='CoverFilm/')

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    publish = models.DateTimeField(default=timezone.now)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager()

    published = PublishedManager()

    class Meta:
        
        ordering = ['-publish']

        indexes = [
            models.Index(fields=['-publish'])
        ]

        verbose_name = 'Product'

        verbose_name_plural = 'Products'

    
    def __str__(self):
        
        return self.title
    

    def get_absolute_url(self):

        return reverse('movie:detail_cinema',args=[self.publish.year,
                                                   self.publish.month,
                                                   self.publish.day,
                                                   self.slug])
    


class Comment(models.Model):

    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE,
                              related_name='comments')
    
    name = models.CharField(max_length=85,verbose_name='Имя')

    email = models.EmailField(verbose_name='почта')

    body = models.TextField(verbose_name='текст')

    created = models.DateField(auto_now_add=True)

    updated = models.DateField(auto_now=True)

    active = models.BooleanField(default=True)

    class Meta:

        ordering = ['-created']

        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = 'Comment'

        verbose_name_plural = "Comments"

    def __str__(self):

        return f"Comment {self.name} by {self.movie}"
    
