#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections, math, random
from datetime import datetime, timedelta
from nltk.metrics.distance import jaccard_distance
from hcde.data.db.base.dbConfig import DBConfiguration
from hcde.data.db.fitness.settings_db import *
from hcde.data.db.fitness.FitTweetsDB import FitTweetsDB as DB
from hcde.data.db.fitness.FitTweetObj import FitTweetObj
from hcde.utils.tweet_entities import tweet_entities
from hcde.utils.stop_words import remove_stops, STOPLIST
from hcde.data.fitness.constants import *
from hcde.data.fitness.tweet_text_doc import tweet_doc


def query_date(db=None, date=None, dur=1, by_hour=False):
    result_list = []
    if( by_hour ):
        delta = timedelta(hours=1)
    else:
        delta = timedelta(days=1)
    dt2 = date + (dur*delta)
    start_date = date.strftime("%Y%m%d%H%M%S")
    end_date = dt2.strftime("%Y%m%d%H%M%S")
    #start_date = date.strftime("%Y%m%d000000")
    #end_date = dt2.strftime("%Y%m%d000000")
    try:
        result_list = db.query_tweet_table_by_date_range(start_date=start_date,
                                                         end_date=end_date,
                                                         in_order=True)
    except Exception, e:
        print "EXCEPTION when running query!"
        print e
        result_list = []
    return {'tweet_list':result_list, 
            'query_date':date, 
            'start_date_str':start_date, 
            'end_date_str':end_date,
            'duration':dur}


def create_tid_dict(tweet_list=[]):
    tdict = {}
    for t in tweet_list:
        tdict[str(t.tweet_id)] = t
    return tdict


def get_comparison_text(key,data={}):
    if( key in data ): return data[key].tweet_text
    return ""


def clustered_key(key,cd):
    if( key in cd['clusters'] ): return True
    key_list = cd['clusters'].keys()
    for k in key_list:
        if( key in cd['clusters'][k] ): return True
    return False


def dump_cluster_info(cluster):
    print "\tclusters count:",len(cluster['clusters']),
    key_list = cluster['clusters'].keys()
    for k in key_list:
        print "(%d)"%(len(cluster['clusters'][k])),
    print
    print "\tgroup_count:",cluster['group_count']
    print "\tgroup_keys count:",len(cluster['group_keys'])
    print "\tthreshold:",cluster['threshold']
    print "\tdata count:",len(cluster['data'])
    print "\tall_keys count:",len(cluster['all_keys'])
    print "\torphan count:",len(cluster['orphans'])


def get_cluster(clust={},cord=0,report=False):
    clist = list()
    if( report ):
        print "There are %d clusters. Picking cluster %d"%(len(clust['clusters']),cord)
    key_list = clust['clusters'].keys()
    key = key_list[cord]
    ckeys = clust['clusters'][key]
    if( report ):
        print "Cluster %d has %d tweets"%(cord,len(ckeys))
    i = 1
    for tid in ckeys:
        clist.append(clust['data'][tid])
        if( report ):
            print "[%03d]::%s::%s"%(i,clust['data'][tid].from_user.encode('utf-8'),clust['data'][tid].tweet_text.encode('utf-8'))
            i+=1
    return clist


def build_tweet_cluster(data={}, cd={}, threshold=0.85, 
                        group_count=-1, report=False):
    if( not cd ):
        cd = dict()
        cd['clusters'] = dict()
        cd['group_count'] = group_count
        cd['group_keys'] = list()
        cd['threshold'] = threshold
        cd['data'] = dict()
        cd['all_keys'] = list()
        cd['orphans'] = list()
    
    if( data ):
        cd['data'].update(data) ## extend a dictionary
        cd['all_keys'].extend(data.keys()) ## extend a list
        
        for k1 in data.keys():            
            # Do we compare by clustered groups?
            if( cd['group_count']>0 ):
                if( len(cd['group_keys'])<cd['group_count'] ):
                    # start building random groups - good, not perfect
                    rk = cd['all_keys'][(random.randint(0,len(cd['all_keys'])-1))]
                    while( clustered_key(rk,cd) ):
                        rk = cd['all_keys'][(random.randint(0,len(cd['all_keys'])-1))]
                    cd['group_keys'].append(rk)
                    if( report ):
                        print "NEW GROUP:",rk
                cluster_keys = cd['group_keys']
            else:
                cluster_keys = cd['all_keys']
            
            dd = {'d':1.0,'k2':"-1"}
            for k2 in cluster_keys:
                if( k1 == k2 ): continue
                if( ((k1 in cd['clusters']) and (k2 in cd['clusters'][k1])) or
                    ((k2 in cd['clusters']) and (k1 in cd['clusters'][k2])) ):
                    continue
                
                tw1 = get_comparison_text(k1,data).split()
                tw2 = get_comparison_text(k2,cd['data']).split()
                if( tw1 and tw2 ):
                    d = jaccard_distance(set(tw1),set(tw2))
                else:
                    d = 1.0
                
                # keep the closest one in the set
                if( d<dd['d'] ):
                    dd['d'] = d
                    dd['k2'] = k2
                
            if( dd['d'] < cd['threshold'] ):
                if( not (dd['k2'] in cd['clusters']) ):
                    cd['clusters'][dd['k2']] = []
                cd['clusters'][dd['k2']].append(k1)
                if( report ):
                    print "Cluster [%s] gets %s (%7.5f)"%(dd['k2'],k1,dd['d'])
            else:
                cd['orphans'].append(k1)
                if( report ):
                    print "ORPHAN! %s (%7.5f)"%(k1,dd['d'])
    return cd


config = DBConfiguration(db_settings=DATABASE_SETTINGS['default'])
db = DB(config=config)

dt = datetime.strptime("20130214150000","%Y%m%d%H%M%S")
day_hr0 = query_date(db=db, date=dt, dur=1, by_hour=True)
print day_hr0['start_date_str'],'-->',day_hr0['end_date_str']

dt = datetime.strptime(day_hr0['end_date_str'],"%Y%m%d%H%M%S")
day_hr1 = query_date(db=db, date=dt, dur=1, by_hour=True)
print day_hr1['start_date_str'],'-->',day_hr1['end_date_str']

dt = datetime.strptime(day_hr1['end_date_str'],"%Y%m%d%H%M%S")
day_hr2 = query_date(db=db, date=dt, dur=1, by_hour=True)
print day_hr2['start_date_str'],'-->',day_hr2['end_date_str']

day_hr0_tid = create_tid_dict(day_hr0['tweet_list'])
day_hr1_tid = create_tid_dict(day_hr1['tweet_list'])
day_hr2_tid = create_tid_dict(day_hr2['tweet_list'])

cluster = build_tweet_cluster(data=day_hr0_tid)
#cluster = build_tweet_cluster(data=day_hr0_tid,report=True)
dump_cluster_info(cluster)

cluster2 = build_tweet_cluster(data=day_hr1_tid)
dump_cluster_info(cluster2)

cluster = build_tweet_cluster(data=day_hr1_tid,cd=cluster)
dump_cluster_info(cluster)

cluster3 = build_tweet_cluster(data=day_hr0_tid, group_count=100)
dump_cluster_info(cluster3)

cluster3 = build_tweet_cluster(data=day_hr0_tid, group_count=100)
dump_cluster_info(cluster3)
cluster3 = build_tweet_cluster(data=day_hr1_tid, cd=cluster3)
dump_cluster_info(cluster3)
c3_c3 = get_cluster(cluster3,3,True)
c3_c5 = get_cluster(cluster3,5,True)
c3_c10 = get_cluster(cluster3,10,True)