from __future__ import unicode_literals
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from .models import *
import youtube_dl, json, datetime, random

ydl_opts= {
    # "quiet":True,
    # "simulate":True
}

#playlist form
class playlist_form(forms.Form):
    url =  forms.CharField(max_length=150,widget = forms.TextInput(attrs={'name':'Playlist URL', 'placeholder':"https://www.youtube.com/playlist?list=..."}),label="Playlist URL")

#user form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

@login_required
def index(request):
    playlist_pks = Playlist.objects.values_list("pk", flat=True)
    return render(request,"youtubedl/index.html",{
            "cs50_playlists":Playlist.objects.filter(categories__name="CS50", date__year=2020),
            "cs50_wt_playlists":Playlist.objects.filter(categories__name="CS50", name__icontains="walkthroughs"),
            "mit_playlists":Playlist.objects.filter(categories__name="MIT OCW", date__year=2020),
            "mit_6_playlists":Playlist.objects.filter(categories__name="MIT OCW", name__contains="MIT 6."),
            "mit_18_playlists":Playlist.objects.filter(categories__name="MIT OCW", name__contains="MIT 18."),
            "random_playlist":Playlist.objects.filter(pk=random.choice(playlist_pks))[0],
        })

@login_required
def playlist(request,id=""):
    if request.method == "GET":
        return render(request,"youtubedl/playlist.html",{
            "playlist":Playlist.objects.filter(pk=id)[0],
        })
    if request.method == "POST":
        videos = Playlist.objects.filter(pk=request.POST["pk"])[0].videos.all()
        playlist = Playlist.objects.filter(pk=request.POST["pk"]) 
        return JsonResponse({"videos":serialize('python',list(videos)),"playlist":serialize('python',list(playlist))},safe=False)

@login_required
def video(request,id=""):
    if request.method == "GET":
        return render(request,"youtubedl/video.html",{
            "video_id":id,
            "playlist":Video.objects.filter(video_id=id)[0].playlist_set.all()[0],
        })

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        form = UserRegisterForm()
    return render(request,"users/register.html",{
        "form":form,
    })

@staff_member_required
def admin_dashboard(request):
    if request.method == "POST":
        if "search" in request.POST:
            return render(request,"admin_dashboard/admin.html",{
            "get_playlist":playlist_form(),
            "playlists":Playlist.objects.filter(name__icontains=request.POST["search"]),
            "search":request.POST["search"],
        })
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info((request.POST["url"]),download=False)
                playlist_date = datetime.datetime.strptime(result['entries'][0]['upload_date'], "%Y%m%d")
                playlist = Playlist(name=result['title'],playlist_id=result['id'],thumbnail=result['entries'][0]['thumbnail'],date=playlist_date)
                playlist.save()
                playlist_duration = 0
                playlist_rating = 0
                playlist_videos_count = 0
                for entry in result['entries']:
                    if entry is not None:
                        video = Video(title=entry['title'],video_id=entry['id'],thumbnail=entry['thumbnail'],date=datetime.datetime.strptime(entry['upload_date'], "%Y%m%d"),duration=entry['duration']//60)
                        video.save()
                        playlist.videos.add(video)
                        playlist_duration += entry['duration'] or 0
                        playlist_rating += entry['average_rating'] or 0
                        playlist_videos_count += 1
                playlist.save()
                playlist.average_rating = (playlist_rating/playlist_videos_count)
                playlist.duration = playlist_duration//(60*60)
                playlist.save()
    return render(request,"admin_dashboard/admin.html",{
            "get_playlist":playlist_form(),
            "playlists":Playlist.objects.all(),
        })

@staff_member_required
def remove(request,id):
        removing_playlist = Playlist.objects.filter(pk=id)[0]
        removing_playlist.videos.all().delete()
        removing_playlist.delete()
        return HttpResponseRedirect(reverse('admin-dashboard'))

@login_required
def search(request):
    if request.method == "GET":
        return HttpResponseRedirect('index')
    if request.method =="POST":
        return render(request,"youtubedl/search.html",{
            "playlists":Playlist.objects.filter(name__icontains=request.POST["search"]),
            "searched":request.POST["search"],
        })

