#Stage 2 Update (Python 3)
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import os
from django.conf import settings
from django.core.exceptions import ValidationError

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
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment



@python_2_unicode_compatible
class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=350)
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name





@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=150)
    news_website = models.ForeignKey(NewsWebsite, blank=True, null=True) 
    description = models.TextField(max_length=500)
    url = models.URLField(max_length=500)
    thumbnail = models.CharField(max_length=500, blank=True)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True,  default=11, on_delete=models.SET_DEFAULT)
    pageweb = models.CharField(max_length=30, blank=True)
    votes   = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    report = models.IntegerField(default=0)



#    def get_absolute_url(self):
#        return reverse('posts:detail', kwargs={'article_id':self.pk})

    def __str__(self):
        return self.pageweb
    def __str__(self):
        return self.title
    @property
    def comments(self):
        article = self
        qs = Comment.objects.filter_by_article(article)
        return qs

    @property
    def get_content_type(self):
        article = self
        content_type = ContentType.objects.get_for_model(article.__class__)
        return content_type



class Profile(models.Model):

  

    user = models.OneToOneField(User)
    avatar = models.FileField(upload_to='profile_image',blank=True) 


    def image_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):

            return self.avatar.url

        else:
            return '/media/profile_image/default-avatar.png' 



    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Profile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(Profile, self).save(*args, **kwargs)


    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


        
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

@receiver(post_save, sender=User)

def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    instance.profile.save()



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


def file_cleanup(sender, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.

    Usage:
    >>> from django.db.models.signals import post_delete
    >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """
    for fieldname in sender._meta.get_all_field_names():
        try:
            field = sender._meta.get_field(fieldname)
        except:
            field = None
        if field and isinstance(field, FileField):
            inst = kwargs['instance']
            f = getattr(inst, fieldname)
            m = inst.__class__._default_manager
            if hasattr(f, 'path') and os.path.exists(f.path)\
            and not m.filter(**{'%s__exact' % fieldname: getattr(inst, fieldname)})\
            .exclude(pk=inst._get_pk_val()):
                try:
                    default_storage.delete(f.path)
                except:
                    pass
