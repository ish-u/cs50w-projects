from __future__ import unicode_literals
from youtubedl.models import *
import youtube_dl, datetime
ydl_opts= {
    'extract_flat':True,
    'quiet':True,
    'ignoreerrors':True,
}
def add(url,pk,start,end):
    num = 1
    with youtube_dl.YoutubeDL(ydl_opts) as y:
        channel = y.extract_info(url,download=False)
        for a in channel['entries'][start:end]:
            print(num,a)
            num += 1
            if a is not None:
                with youtube_dl.YoutubeDL({'ignoreerrors':True}) as ydl:
                    result = ydl.extract_info((a['url']),download=False)
                    playlist_date = datetime.datetime.strptime(result['entries'][0]['upload_date'], "%Y%m%d")
                    playlist = Playlist(name=result['title'],playlist_id=result['id'],thumbnail=result['entries'][0]['thumbnail'],date=playlist_date)
                    playlist.save()
                    playlist_duration = 0
                    playlist_rating = 0
                    playlist_videos_count = 0
                    for a in result['entries']:
                        if a is not None:
                            video = Video(title=a['title'],video_id=a['id'],thumbnail=a['thumbnail'],date=datetime.datetime.strptime(a['upload_date'], "%Y%m%d"),duration=a['duration']//60)
                            video.save()
                            playlist.videos.add(video)
                            playlist_duration += a['duration'] or 0
                            playlist_rating += a['average_rating'] or 0
                            playlist_videos_count += 1
                    playlist.save()
                    playlist.average_rating = (playlist_rating/playlist_videos_count)
                    playlist.duration = playlist_duration//(60*60)
                    category = Category.objects.filter(pk=pk)[0]
                    playlist.categories.add(category)
                    playlist.save()

