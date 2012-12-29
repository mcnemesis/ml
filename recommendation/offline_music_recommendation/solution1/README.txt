This is Solution 1 to the given offline music recommendation problem.

I have tested it on my machine, and I surely are very happy with the results (music recommendations)
given so far.

-----------------

The solution is a python program, whose Recommendation Engine might be used by other programs
using this sort of approach for example:

    collection_path = '/media/planet/Ziki'
    r = RecommendationEngine(collection_path,ffilter=r'^.+\.(mp3|mp4|flv|wma)$')

    request_datetime = datetime.now()
    recommendation_size = 5
    
    playlist = r.recommend(request_datetime,recommendation_size)

In the above, playlist will contain a list of music file paths (the filter specifying what files are of interest is
specified as a regular expression in the ffilter param -- defaults to r'^.+\.(mp3)$').

We also are setting the request time of reference as the current datetime, and are further telling the engine to only 
recommend a maximum of 5 items in the playlist.

--------------------

The existing solution script can also be directly used on the command-line to obtain a list of recommended songs as a 
list of files/ paths. Such a usage could come in handy where one needs to further pre-process the list of files prior
to say feeding them to their music player of choice. An example of this mode, just printing the list of files is:

./music_suggest.py /media/planet/Ziki/TECHNIX/DARKSTEP/ 5

"/media/planet/Ziki/TECHNIX/DARKSTEP/Donny - The Forgotten (Current Value Remix).mp3"
"/media/planet/Ziki/TECHNIX/DARKSTEP/Agnost1k Podcast 04 – Dither~/AGN PODCAST_04/Dither Cast.mp3"
"/media/planet/Ziki/TECHNIX/DARKSTEP/AIRJ SET TRACKS JANUARY 2012.mp3"
"/media/planet/Ziki/TECHNIX/DARKSTEP/Akira @ the Arches Glasgow, St Valentines Party 2012.mp3"
"/media/planet/Ziki/TECHNIX/DARKSTEP/Cerebral_Destruction_Podcast_001_featuring_Frazzbass.mp3"


---------------------

But to make things much more easy, and fun. I have provided a script that automatically would recommend and play the 
recommended songs in vlc. Note that u can change the hard-coded path passed as a parameter to the script (including the 
above use-case), so as to point to where u want the music to be sampled from.

./suggest_vlc.sh /media/planet/Ziki/ETHNIC/ 10


NOTE : 
======
I've modified the Recommendation Engine to also be able to recommend what it finds to be the most rarely played music in the 
collection. For this mode, just pass an extra parameter to the invocations above ('best' for normal mode, else it's the rare mode)

For example:

./music_suggest.py /media/planet/Ziki/TECHNIX/DARKSTEP/ 5 rare

or 

./suggest_vlc.sh /media/planet/Ziki/ETHNIC/ 10 rare
