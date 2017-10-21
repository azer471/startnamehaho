#Stage 2 Update (Python 3)
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from scrapy_djangoitem import DjangoItem
from dynamic_scraper.models import Scraper, SchedulerRuntime

from django.contrib.auth.models import User
from django.db.models.signals import post_save


from datetime import datetime  

#form
from django.core.urlresolvers import reverse
#from django.core.validators import RegexValidator

@python_2_unicode_compatible
class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name






@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=130)
    news_website = models.ForeignKey(NewsWebsite) 
    description = models.TextField(max_length=500)
    url = models.URLField(max_length=200)
    thumbnail = models.CharField(max_length=200, blank=True)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True,  default=1)
    pageweb = models.CharField(max_length=30)

    votes   = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    

#    def get_absolute_url(self):
#        return reverse('posts:detail', kwargs={'article_id':self.pk})

    def __str__(self):
        return self.pageweb
    def __str__(self):
        return self.title

class ArticleItem(DjangoItem):
    django_model = Article


@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, NewsWebsite):
        if instance.scraper_runtime:
            instance.scraper_runtime.delete()
    
    if isinstance(instance, Article):
        if instance.checker_runtime:
            instance.checker_runtime.delete()
            
pre_delete.connect(pre_delete_handler)



##################
class Voter(models.Model):
    article = models.ForeignKey(Article)


