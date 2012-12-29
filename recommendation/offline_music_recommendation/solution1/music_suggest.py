#!/usr/bin/env python

import os
from datetime import datetime,timedelta
import re


class Entity:
    file_filter = r'^.+\.(mp3)$'

    def __init__(self,path,parent=None,ffilter=None):
        self.path = path
        self.is_file = Entity.path_is_file(path)
        self.most_recent_member_atime = 0
        self.number_plays = 0
        self.parent  = parent
        self.members = []

        if filter is not None:
            self.file_filter = ffilter

        self.evaluate_members()

        self.rank = 0

    def set_most_recent_atime(self,atime):
        if atime > self.most_recent_member_atime:
            self.most_recent_member_atime = atime
            if self.parent:
                self.parent.set_most_recent_atime(atime)

    def set_number_plays(self,plays):
        if self.is_file:
            self.number_plays = plays
            if self.parent:
                self.parent.set_number_plays(plays)
        else:
            self.number_plays += plays
            if self.parent:
                self.parent.set_number_plays(plays)

    def get_number_plays(self):
        return self.number_plays

    def evaluate_members(self):
        if self.is_file:
            self.most_recent_member_atime = os.stat(self.path).st_atime
            self.parent.set_most_recent_atime(self.most_recent_member_atime)
            #the number of plays for a file would have ideally been obtained from some index/db of sorts recorded over-time
            #/but, for simplicity in the current implementation, we shall assume all files have only been played once, by default
            self.set_number_plays(1)
        else:
            for p in os.listdir(self.path):
                path = os.path.join(self.path,p)

                if Entity.path_is_file(path):
                    if re.match(Entity.file_filter,path) is not None:
                        self.members.append(Entity(path,parent=self,ffilter=self.file_filter))
                else:
                    self.members.append(Entity(path,parent=self,ffilter=self.file_filter))

    def get_most_recent_member_access_time(self):
        return self.most_recent_member_atime

    def calculate_rarity_rank(self,request_datetime):

        atime = datetime.fromtimestamp(self.get_most_recent_member_access_time())
        
        radiff = (request_datetime - atime).seconds 

        self.rank = (1 - 1.0 / radiff  ) * self.get_number_plays()

    def calculate_rank(self,request_datetime):
        epoch = datetime(year=1970,month=1,day=1)

        atime = datetime.fromtimestamp(self.get_most_recent_member_access_time())
        t = atime.time()

        atime = epoch + timedelta(hours=t.hour,minutes=t.minute,seconds=t.second)

        t = request_datetime.time()
        request_datetime = epoch + timedelta(hours=t.hour,minutes=t.minute,seconds=t.second)
        
        radiff = (request_datetime - atime).seconds 

        #print "radiff: %s , plays : %s " % (radiff,self.number_plays)

        self.rank = ( 1.0 / radiff  ) * self.get_number_plays()

    def get_best_members(self,request_datetime,size):
        from random import sample

        map(lambda m : m.calculate_rank(request_datetime), self.members)

        if self.is_file:
            return [self]
        else:
            best = []

            for member in self.members:
                best.extend(member.get_best_members(request_datetime,size))

            best_list = sorted(best,key=lambda m: m.rank)[0:size * 2]

            best_list = sample(best_list,min(size,len(best_list)))

            return best_list

    def get_rarest_members(self,request_datetime,size):
        from random import sample

        map(lambda m : m.calculate_rarity_rank(request_datetime), self.members)

        if self.is_file:
            return [self]
        else:
            best = []

            for member in self.members:
                best.extend(member.get_best_members(request_datetime,size))

            best_list = sorted(best,key=lambda m: m.rank)[0:size * 2]

            best_list = sample(best_list,min(size,len(best_list)))

            return best_list

    def __repr__(self):
        return "%s : r:%s | p:%s { %s }" % (
                "File" if self.is_file else "Dir",
                self.rank,
                self.number_plays,
                self.path
                )

    @staticmethod
    def path_is_file(path):
        return os.path.isfile(path)

class RecommendationEngine:
    def __init__(self,music_base,ffilter=r'^.+\.(mp3)$'): #only mp3 by default
        self.collection = Entity(music_base,ffilter=ffilter)

    def recommend_best(self,request_datetime,size):
        return self.collection.get_best_members(request_datetime,size)

    def recommend_rarest(self,request_datetime,size):
        return self.collection.get_rarest_members(request_datetime,size)

if __name__ == '__main__':
    import sys

    collection_path = '/media/planet/Ziki'
    recommendation_size = 1
    mode = 'best'

    if len(sys.argv) == 2:
        collection_path = os.path.expanduser(sys.argv[1])
    elif len(sys.argv) == 3:
        collection_path = os.path.expanduser(sys.argv[1])
        recommendation_size = int(sys.argv[2])
    elif len(sys.argv) == 4:
        collection_path = os.path.expanduser(sys.argv[1])
        recommendation_size = int(sys.argv[2])
        mode = sys.argv[2]

    if os.path.exists(collection_path):
        if recommendation_size > 0:
            r = RecommendationEngine(collection_path,ffilter=r'^.+\.(mp3|mp4|flv|wma)$')
            request_datetime = datetime.now()

            playlist = r.recommend_best(request_datetime,recommendation_size) if mode == 'best' else r.recommend_rarest(request_datetime,recommendation_size)
            
            for p in playlist:
                print '"%s"' % p.path 
