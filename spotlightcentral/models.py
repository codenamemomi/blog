from django.db import models
from django.utils import timezone
from django.db.models.functions import Now
from django.conf import settings
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
            )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='spotlightcentral_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager()       #default manager
    published = PublishedManager()   #my custom manager

    class Meta:
        ordering = ['-publish']
        # this is the index option to improve performance for query filtering or ordering results by this field

        indexes = [
            models.Index(fields=['-publish'], name='post_publish_idx'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'spotlightcentral:post_detail',
            args=[self.publish.year,
                  self.publish.month,
                  self.publish.day,
                  self.slug
                  ]
        )
    
    def save(self, *args, **kwargs):
        if self.status == self.Status.PUBLISHED and not self.publish:
            self.publish = timezone.now()
        super().save(*args, **kwargs)