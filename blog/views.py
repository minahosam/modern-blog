from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from django.db.models import Count

# Create your views here.
def home(request):
    all_posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[:3]
    recent_posts = Post.objects.all().order_by('-updated')[:3]
    featured_post = Post.objects.filter(is_published=True)
    if featured_post:
        featured_post = featured_post[0]
    websiteInfo = None
    if WebsiteMeta.objects.all():
        websiteInfo = WebsiteMeta.objects.all()[0]
    context = {'all_posts': all_posts, 'top_posts': top_posts, 'recent_posts': recent_posts, 'featured_post': featured_post,'websiteInfo': websiteInfo}
    return render(request,'blog/index.html', context)

def post_detail(request,slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        post = None
    comments = None
    count = None
    if post:
        comments = Comment.objects.filter(post=post,parent=None)
        count = comments.count()
    form = commentForm()
    if request.method == 'POST':
        comment = commentForm(request.POST)
        parent = None
        if request.POST.get('parent'):
            par = request.POST.get('parent')
            father = Comment.objects.get(pk=par)
            # parent = Comment.objects.get(parent=father)
            if father:
                comment_reply = comment.save(commit=False)
                comment_reply.parent = father
                comment_reply.author = request.user
                comment_reply.post = post
                comment_reply.save()
                return HttpResponseRedirect(reverse('home:post_detail',kwargs={'slug': slug}))
        else:
            comment_post = comment.save(commit=False)
            comment_post.parent = parent
            comment_post.post = post
            comment_post.author = request.user
            comment_post.save()
            print('---------------'+slug)
            return HttpResponseRedirect(reverse('home:post_detail',kwargs={'slug': slug}))
    if post:
        if post.view_count == 0:
            post.view_count = 1
            post.save()
        else:
            post.view_count += 1
            post.save()
    context = {'post': post,'form': form,'comments': comments,'count':count}
    return render(request,'blog/Post_detail.html',context)

def tag_detail(request,slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tag__in=[tag.id]).order_by('-view_count')[:2]
    recent_posts = Post.objects.filter(tag__in=[tag.id]).order_by('-updated')[:2]
    tags = Tag.objects.all()
    context = {'tags': tags, 'recent_posts': recent_posts,'tag': tag, 'top_posts':top_posts}
    return render(request,'blog/tag_detail.html',context)

def profile_page(request,slug):
    me = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=me.id).order_by('-view_count')[:2]
    recent_posts = Post.objects.filter(author=me.id).order_by('-updated')[:2]
    top_authors = User.objects.annotate(number=Count('post_author')).order_by('-number')
    context = {'top_posts':top_posts, 'recent_posts':recent_posts,'top_authors':top_authors,'me':me}
    return render(request,'blog/author_page.html', context)

def search_posts(request):
    search_query = None
    search_result = None
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    if search_query:
        search_result = Post.objects.filter(title__icontains=search_query)
    context = {'search_result':search_result}
    return render(request,'blog/search.html', context)