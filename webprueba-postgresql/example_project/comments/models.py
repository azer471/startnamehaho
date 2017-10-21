from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.urlresolvers import reverse

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs
    def filter_by_article(self, article):
        content_type = ContentType.objects.get_for_model(article.__class__)
        obj_id = article.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)
        return qs

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent      = models.ForeignKey("self", null=True, blank=True)


    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    votes_comment   = models.IntegerField(default=0)

    objects = CommentManager()
    class Meta:
        ordering = ['-timestamp']
    def __unicode__(self):
        return str(self.author)

    def __str__(self):
        return str(self.author)


    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:votes_comment", kwargs={"id": self.id})

        
    def children(self): #replies
        return Comment.objects.filter(parent=self)
    

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

class Vvoter(models.Model):
    comment = models.ForeignKey(Comment)
