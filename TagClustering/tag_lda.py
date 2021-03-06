#!/usr/bin/env python3
import datetime
import numpy
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(PACKAGE_PARENT)

import Liu.custommodule.locationcluster as ccluster
import Liu.custommodule.lda as clda
import Liu.custommodule.location as clocation
import Liu.custommodule.tag as ctag
import Liu.custommodule.user as cuser

"""parameters"""
#1443672000 # 2015/10/01 #1446350400 # 2015/11/01 #1447560000 # 2015/11/15 #1448942400 # 2015/12/01 #1451620800 #2015/01/01 @UCT-4
FILTER_TIME_S = 1443672000 
FILTER_TIME_E = 1446350400 
TOPIC_NUM = 35


"""file path"""
USER_TAGS_FILE = "./data/LocationTags"
USER_POSTS_FILE = "./data/TravelerPosts"
OUTPUT_TAG_TOPIC = "./data/LocationTopic/TagTopic_OCT_c" + str(TOPIC_NUM) + ".txt"
OUTPUT_LOCATION_TOPIC = "./data/LocationTopic/LocationTopic_OCT_c" + str(TOPIC_NUM) + ".txt"


def main():
    print("--------------------------------------")
    print("STARTTIME:", (datetime.datetime.now()))
    print("--------------------------------------")

    # getting data
    #locations = ctag.open_location_tags(USER_TAGS_FILE)

    #corpus = ctag.get_corpus([x.tags for x in locations.values()])

    # getting data - way 2
    locations = clocation.open_locations()
    users = cuser.open_users_posts_afile(USER_POSTS_FILE)
    print("Sampling users posts...")
    for key, a_user in users.items():
        posts = [x for x in a_user.posts if (x.time > FILTER_TIME_S) and (x.time < FILTER_TIME_E)]
        users[key].posts = posts
    locations = clocation.fit_users_to_location(locations, users, "tags")

    corpus = ctag.get_location_posts_corpus(locations)
    
    vector, tag_name = clda.get_tag_vector(corpus)
    topic_word, doc_topic = clda.fit_lda(vector, tag_name, TOPIC_NUM)
    ccluster.output_topics(topic_word, doc_topic, tag_name, [x.lid for x in locations.values()], OUTPUT_TAG_TOPIC, OUTPUT_LOCATION_TOPIC)

    print("--------------------------------------")
    print("ENDTIME:", (datetime.datetime.now()))
    print("--------------------------------------")

if __name__ == '__main__':
    main()
