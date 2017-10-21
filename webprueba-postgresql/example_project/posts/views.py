from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Voter, Profile



from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q, Count
import operator

#from
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from .forms import ArticleCreate, UserForm, DocumentForm
#User
from  django.contrib.auth import authenticate, login
from django.views.generic import View
#profile page
from django.db import models
from django.forms import ModelForm

from django.views.generic.detail import DetailView
from django.contrib.auth.models import User




from django.db.models import Avg


import datetime
#comment
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment, Vvoter
from comments.forms import CommentForm

#change password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect




def index(request):
  
    post_list = Article.objects.order_by('-id').filter(approved=True)
    query = request.GET.get("q")
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
            ).distinct()


    paginator = Paginator(post_list, 25)


    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        blogs = paginator.page(page)
    except(EmptyPage, InvalidPage):
        blogs = paginator.page(1)

    # Get the index of the current page
    index = blogs.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # My new page range
    page_range = paginator.page_range[start_index:end_index]




    time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    title_day = Article.objects.filter(created_date__gte=time_24_hours_ago,approved=True).order_by('-votes')
    if not title_day:
        title_day = Article.objects.order_by('-id').filter(approved=True)


    time_week = datetime.datetime.now() - datetime.timedelta(days=7)
    title_week = Article.objects.filter(created_date__gte=time_week,approved=True).order_by('-votes')
    if not title_week:
        title_week = Article.objects.order_by('-id').filter(approved=True)




    return render(request, 'posts/index.html', {
        'blogs': blogs,
        'page_range': page_range,
        'title_day':title_day,
        'title_week':title_week,
    })



def profile(request,username):
  
    user = User.objects.get(username=username)



    logged_in_user_posts = Article.objects.filter(author=user)
    posts_count = Article.objects.filter(author=user).count()
    posts_count_votes = Article.objects.filter(author=user).aggregate(Avg('votes'))['votes__avg']


    paginator = Paginator(logged_in_user_posts, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        blogs = paginator.page(page)
    except(EmptyPage, InvalidPage):
        blogs = paginator.page(1)

    # Get the index of the current page
    index = blogs.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # My new page range
    page_range = paginator.page_range[start_index:end_index]

######################

    comments = Comment.objects.filter(author=user)
    comments_count = comments.values('parent').annotate(the_count=Count('parent'))      

######################

   
#####"
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return HttpResponse("invalid user_profile!")

    if request.method == "POST":

        update_profile_form = DocumentForm(data=request.POST, instance=user_profile)

    
        profile = update_profile_form.save(commit=False)
        profile.user = user

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()

    else:

        update_profile_form = DocumentForm(instance=user_profile)
#####

    if request.method == 'POST' and not 'avatar' in request.FILES:
        form_passw = PasswordChangeForm(request.user, request.POST)
        if form_passw.is_valid():
            user = form_passw.save()
            update_session_auth_hash(request, user)  # Important!
            messages.info(request, 'تم تغيير كلمة السر بنجاح!')

        else:
            messages.error(request, 'يرجى تصحيح الخطأ')
    else:
        form_passw = PasswordChangeForm(request.user)

    return render(request, 'posts/profile.html', {




        'comments_count':comments_count,
        'comments':comments,
     
        'posts': logged_in_user_posts,'blogs': blogs,
        'page_range': page_range,
        'posts_count': posts_count,
  
        'user':user,
        'posts_count_votes':posts_count_votes,

'update_profile_form': update_profile_form,
 'form_passw': form_passw

   
        })





def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)



    initial_data = {
            "content_type": article.get_content_type,
            "object_id": article.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")

        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
                
        new_comment, created = Comment.objects.get_or_create(
                            author = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                       

                         
                        )
        return HttpResponseRedirect(reverse('posts:detail', args=[article.id]))
    comments = article.comments 




###########
    time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    title_day = Article.objects.filter(created_date__gte=time_24_hours_ago).order_by('-votes')
    if not title_day:
        title_day = Article.objects.order_by('-id')


    time_week = datetime.datetime.now() - datetime.timedelta(days=7)
    title_week = Article.objects.filter(created_date__gte=time_week).order_by('-votes')
    if not title_week:
        title_week = Article.objects.order_by('-id')
###########








    return render(request, 'posts/detail.html', {'article':article,
        'comments':comments,
        'comment_form':form,
        'title_day':title_day,
        'title_week':title_week,
        })












def post_new(request):
    if request.method == "POST":
        form = ArticleCreate(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.approved= False
            post.save()
            return HttpResponseRedirect(reverse('posts:detail', args=[post.id]))

    else:
        form = ArticleCreate()
    return render(request, 'posts/article_form.html', {'form': form})





class UserFormView(View):
    form_class = UserForm
    template_name= 'posts/registration_form.html'


    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render (request, self.template_name, {'form':form})
       
    #proces form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
       
            #cleaned(normalized) data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)

            user.save()
           

            #returns User objects if credencials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('posts:index')

        return render (request, self.template_name, {'form':form})

def votes_comment(request, comment_id):
    if request.method == 'POST':
        if request.is_ajax():
            up_down = request.POST.get('up_down')
            comment = Comment.objects.get(pk=comment_id) 
            if Vvoter.objects.filter(comment_id=comment_id).exists():

                return render('posts/detail.html', {
                    'error_message': "Sorry, but you have already voted."
                })                       
    
            if up_down == "plus":
      
                comment.votes_comment += 1
                comment.save()
                Vvoter.objects.create(comment_id=comment_id)
            
            else:
             
                comment.votes_comment -= 1
                comment.save()
                Vvoter.objects.create(comment_id=comment_id)
              
            data = {"votes_comment": comment.votes_comment}
            return JsonResponse(data)

    return HttpResponseRedirect(reverse('posts:index'))



def vote(request, article_id):
    if request.method == 'POST':
        if request.is_ajax():
            up_down = request.POST.get('up_down')
            article = get_object_or_404(Article, pk=article_id)
            if Voter.objects.filter(article_id=article_id).exists():

                return render('posts/detail.html', {
                    'error_message': "Sorry, but you have already voted."
                })           
            
            if up_down == "plus":
                article.votes += 1
                article.save()
                Voter.objects.create(article_id=article_id)
            else:
                article.votes -= 1
                article.save()
                Voter.objects.create(article_id=article_id)
            data = {"votes": article.votes}
            return JsonResponse(data)

    return HttpResponseRedirect(reverse('posts:index'))

def report(request, article_id):
    if request.method == 'GET':
        if request.is_ajax():
            print ('button report working!!!')
            up = request.GET.get('up')
            article = get_object_or_404(Article, pk=article_id)
            if Voter.objects.filter(article_id=article_id).exists():

                return render('posts/detail.html', {
                    'error_message': "Sorry, but you have already voted."
                })                  
      
            
  
            article.report += 1
            article.save()
            Voter.objects.create(article_id=article_id)            
            if article.report==15:
                article.delete()

            data = {"report": article.report}
            return JsonResponse(data)

    return HttpResponseRedirect(reverse('posts:index'))






class ArticleDetail(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        self.object.add_visit()
        self.object.save()
        return context