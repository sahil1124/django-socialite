from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post,Profile,Like,Comment,Following
from django.contrib import messages
import json
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.core.paginator import Paginator
from django.views.generic import ListView
# Create your views here.
@login_required
def userHome(request):
    user=Following.objects.get(user=request.user)

    # followed_user=[i for i in user.followed.all()]
    # followed_user.append(request.user)

    followed_user=user.followed.all()


    posts=Post.objects.filter(user__in=followed_user).order_by('-pk') | Post.objects.filter(user=request.user).order_by('-pk')
    liked_post=[]
    for i in posts:
        is_liked=Like.objects.filter(post=i,user=request.user)
        if is_liked:
            liked_post.append(i)

    paginator=Paginator(posts,5)
    page=request.GET.get('page')
    posts=paginator.get_page(page)
    context={'posts':posts,'liked_post':liked_post}
    return render(request,'userpage/postfeed.html',context)

def post(request):
    if request.method=="POST":
        image_=request.FILES['image']
        captions_=request.POST.get('captions','')
        user_=request.user
        print(image_,captions_)

        post_obj=Post(user=user_ , image=image_ , caption=captions_)
        post_obj.save()


        messages.success(request,'post success Posted')
        return redirect('/userpage')
    else:
        messages.error(request,'no post')
        return redirect('/userpage')

def delPost(request,ID):
    post_=Post.objects.filter(pk=ID)
    image_path=post_[0].image.url
    post_.delete()
    messages.info(request,'Post is Deleted!!')
    return redirect('/userpage')

def userProfile(request,username):
    user=User.objects.filter(username=username)
    if user:
        profile=Profile.objects.get(user=user[0])
        post=getPost(user)
        bio=profile.bio
        connection=profile.connection
        user_img=profile.userImage
        username=user[0].username
        is_following=Following.objects.filter(user=request.user,followed=user[0])  # or followed__in=user ,because followed is object of multiple users
        following_obj=Following.objects.get(user=user[0])
        follower,following=following_obj.follower.count(),following_obj.followed.count()


        context={'username':username,
                 'profile':profile,
                 'user_obj':user,
                'bio':bio,
                'connection':connection,
                'follower':follower,
                'following':following,
                'userImg':user_img,
                'posts':post,
                'is_followings':is_following
                }
    else:
        return HttpResponse("No such user")
    return render(request,'userpage/userProfile.html',context)

def getPost(user):
    post_obj=Post.objects.filter(user=user[0])
    imgList=[post_obj[i:i+3] for i in range(0,len(post_obj),3)]
    return imgList

@login_required
def likePost(request,ID):
    post_id=request.GET.get("likeId",'')
    post=Post.objects.get(pk=post_id)
    user=request.user
    like=Like.objects.filter(post=post,user=user)
    liked=False

    if like:
        Like.dislike(post,user)
    else:
        liked=True
        Like.like(post,user)


    resp={
        'liked':liked
    }

    response=json.dumps(resp)
    return HttpResponse(response,content_type="application/json")

@login_required
def comment(request,pk):
    post=get_object_or_404(Post,pk=pk)
    user=request.user
    comments = post.comments.filter(active=True)
    new_comment=None

    if request.method == 'POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            return redirect('/userpage')


    else:
        form=CommentForm()
    return render(request,'userpage/comment.html',{'post':post,'user':user,'new_comment':new_comment,'form':form,'comments':comments})



    # post=get_object_or_404(Post,pk=pk)
    # comment=request.POST.get('comment','')
    # user=request.user
    # comment_obj=Comment.objects.create(post=post,user=user,text=comment)
    # comment_obj.save()
    # messages.success(request,'Comment Successfully Posted')
    # context={'comment_obj':comment_obj}
    # return render(request,'userpage/comment.html',context)





    # else:
    #     messages.error(request,'no coment')
    #     return redirect('/userpage')




def follow(request,username):
    main_user=request.user
    to_follow=User.objects.get(username=username)

    #check if already following user
    following=Following.objects.filter(user=main_user,followed=to_follow)
    is_following=  True if following else False

    if is_following:
        #then unfollow the user
        Following.unfollow(main_user,to_follow)
        is_following=False
    else:
        Following.follow(main_user,to_follow)
        is_following=True

    resp={
        'following':is_following
    }

    response=json.dumps(resp)
    return HttpResponse(response,content_type="application/json")


class SearchUser(ListView):
    model=User
    template_name='userpage/search.html'


    def get_queryset(self):
        username=self.request.GET.get('username','')
        print(username)
        queryset=User.objects.filter(username__icontains=username)
        print(queryset)
        return queryset
