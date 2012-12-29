An Offline Music Recommendation Algorithm:
------------------------------------------

Problem : 
-----------

I have a vast collection of music stored on my disk. I occassionally browse through it, and 
play a song or two. Often, am very particular about kind of music I can listen to at a given time
and day (of the week). Am often busy, and don't wish to waste time finding what music to play when 
the need to listen to something arises, thus I wish to have my computer automatically suggest the most
adequate song(s) for me to listen to based on time of day, day of the week and previous likes / dislikes.

One thing that can readily be exploited by the algorithm is that I tend to place similar types of music in the same
directory/ folder.


Solution 1:
---------------

1. Create an index of the available music collection, holding info about the music collection:

    Music File : date last played(last access time), number of times played (to be counted on every subsequent play by indexing agent)

    Music Directory : date last played (same as that of most recent played member file), number of times played (sum of #plays of all member files)


2. Given a Request (we are only interested in the date and time):
    1. Recursively (Directories > Directories, Files) Rank the contents of the music collection based on #plays > datetime last played
    2. Pick the top N high-ranking members, recursively continuing the process for directory members, until u have N files selected.
        To accomodate some allowance for trying out new music, randomly select a file from a directory, though give more weight to high-ranking
        files.
    2. Pick K nearest neighbors to the request date and time from the N selected above
    3. Randomly pick S files from the above K neighbors to play, sorted by rank


    To Rank a Member(Directory/File):

    Rank(Member) = absolute[time(request_datetime) - time(lastaccess_datetime)]/ time(request_datetime) * (number_of_plays + 1)

    lastaccess_datetime(File) == last access timestamp of file
    number_of_plays(File) == total tally for everytime we confirm file was played (could be stored in a db)

    lastaccess_datetime(Directory) == most_recent( list of lastaccess_datetime(MemberFile) )
    number_of_plays(File) == sum( list of number_of_plays(MemberFile) )
