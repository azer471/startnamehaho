from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Voter



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
from .forms import ArticleCreate, UserForm
#User
from  django.contrib.auth import authenticate, login
from django.views.generic import View
#profile page
from django.db import models
from django.forms import ModelForm

from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

def index(request):
    post_list = Article.objects.order_by('-id')

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

    return render(request, 'posts/index.html', {
        'blogs': blogs,
        'page_range': page_range,
    })







def profile(request,username):
    article = User.objects.filter(username=request.user)



    logged_in_user = request.user
    logged_in_user_posts = Article.objects.filter(author=logged_in_user)
    posts_count = Article.objects.filter(author=logged_in_user).count()


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
    print (article)


    return render(request, 'posts/profile.html', {'posts': logged_in_user_posts,'blogs': blogs,
        'page_range': page_range,'posts_count': posts_count,'profile':profile,'article':article,})

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)



    return render(request, 'posts/detail.html', {'article':article})


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





def post_new(request):
    if request.method == "POST":
        form = ArticleCreate(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
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

