#Stage 2 Update (Python 3)
from __future__ import unicode_literals
from django.contrib import admin
from posts.models import NewsWebsite, Article, Profile



from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User






class NewsWebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_', 'scraper')
    list_display_links = ('name',)
    
    def url_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.url, title=instance.url)
    url_.allow_tags = True
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'approved','title','description','pageweb','url','report')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)




admin.site.register(NewsWebsite, NewsWebsiteAdmin)
admin.site.register(Article, ArticleAdmin)
