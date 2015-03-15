import os
import sys
import tweepy
import datetime
#mport urllib
import signal
import json
import boto
from boto.s3.connection import S3Connection
#import tweetserializer
#import tweetanalyzer
from boto.s3.key import Key
#import numpy as np
#import pylab as pl
import pymongo

try:
   mongoConnection = pymongo.MongoClient()
except:
   print "Connection failed"
   exit()
#create table
db_streamT = mongoConnection['twitter_analyzer'].db_streamT

aws_access_key_id =''
aws_secret_access_key= ''
aws_bucket_name=''


s3conn = S3Connection(aws_access_key_id,aws_secret_access_key)
bucket = s3conn.get_bucket(aws_bucket_name)

#get tweets from S3 and dump them into db_streamT
for key in bucket.list():
           #each file contains 500 tweets, split them up and put each tweet json data into the table
           key.get_contents_to_filename("fromS3/" + key.name)
           directory = os.getcwd() + "/fromS3"
           filer = open(directory +"/"+ key.name,"r")
           data=json.loads(filer.read())
           #tweets =  {"name":key.name,"fileContent": filer.read()}
           #db_streamT.insert(tweets)
           filer.close()
           #file was read into memory, now delete it to save disk space
           os.remove(directory+"/"+key.name)
           for tweet in data:
                 temp = {"id":tweet['id'],"tweetJson":tweet}
                 db_streamT.insert(temp)
                 

