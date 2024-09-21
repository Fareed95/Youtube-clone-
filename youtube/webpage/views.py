from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Video, Channel, Comment



@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    if request.method =='GET' : 
        return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('video_feed')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    if request.method =='GET':
        return render (request,'login.html')

def LogoutPage(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login')


def video_feed(request):
    if request.method == "GET":
        videos = Video.objects.all()
        context ={
            'videos': videos
            }
       
        return render(request, 'video_feed.html',context )
    if request.method == 'POST':
        pass

def video_detail(request, pk):
    if request.method == "GET":
        videos = Video.objects.all()
        video_personal = get_object_or_404(Video, id=pk)
        
        context = {
            'video_personal': video_personal,
            'videos': videos,
                }
        return render(request, 'video_detail.html', context)
    if request.method == "POST":
        pass

@login_required(login_url='login')
def channel_detail(request, pk):
    if request.method == "GET":
        channel = get_object_or_404(Channel, pk=pk)
        videos = channel.videos.all()  
        context =  {'channel': channel, 'videos': videos}
        return render(request, 'channel_detail.html',context)
    if request.method == "POST":
        pass
@login_required(login_url='login')
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == "POST":
        if request.user in video.liked_by.all():
            video.liked_by.remove(request.user)  # Remove user from liked_by
        else:
            video.liked_by.add(request.user)  # Add user to liked_by

        video.save()  # Save the changes
        return redirect('video_detail', pk=video.id)  # Redirect to the video detail page
    else:
        return HttpResponse(status=405)


@login_required(login_url='login')
def add_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        channel_id = request.POST.get('channel')
        
        channel = get_object_or_404(Channel, id=channel_id)
        author = request.user  

        new_video = Video.objects.create(
             title=title,
            description=description,
            video_file=video_file,
            thumbnail=thumbnail,
            channel=channel,
            author=author
        )
        new_video.save()
        
        return redirect('video_feed')
    
    channels = Channel.objects.all() 
    context = {'channels': channels}
    return render(request, 'add_video.html', context)


@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        content = request.POST.get('content').strip()  # Prevent empty or whitespace-only comments
        if not content:
            return HttpResponse("Comment cannot be empty!", status=400)
        
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None
        Comment.objects.create(user=request.user, video=video, content=content, parent_comment=parent_comment)
        
        return redirect('video_detail', pk=video.id)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.user in comment.liked_by.all():
            comment.liked_by.remove(request.user)
            comment.likes -= 1
        else:
            comment.liked_by.add(request.user)
            comment.likes += 1
        comment.save()
        return JsonResponse({'likes': comment.likes})

    return HttpResponse(status=405)