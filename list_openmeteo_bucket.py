#! /usr/bin/python
# -*- coding:utf-8 -*-
import boto3
import requests
arn="arn:aws:s3:::mf-nwp-models"
  #  arn:aws:s3:::mf-nwp-models
   # arn:aws:s3:::examplebucket/*
#"s3://mf-models-on-aws/{MODEL}/v2/{YYYY-MM-DD}/{HH}/{PARAMETER}/{LEVEL_TYPE}/{TIMESTEP}.grib2"
    #arn:aws:s3:::bucket_name/key_name
  #  https://s3.Region.amazonaws.com/bucket-name/key name
  #  https://bucket-name.s3.Region.amazonaws.com/key name
"""
url="https://mf-nwp-models.s3.eu-west-1.amazonaws.com"
url="https://s3.eu-west-1.amazonaws.com/mf-nwp-models"
status=0
while status != 200:
    r=requests.get(url)      # acquisition de la page HTML
    status=r.status_code
    #print (status)
res=r.content
print(res)

region="eu-west-1"
res = boto3.resource('s3')
bucket = res.Bucket(arn)
for obj in bucket.objects.all():
    print(obj.key)
"""
client = boto3.client('s3')
paginator = client.get_paginator('list_objects')
result = paginator.paginate(Bucket=arn, Delimiter='/')
for prefix in result.search('CommonPrefixes'):
    print(prefix.get('Prefix'))


"""
#objets=bucket.get_available_subresources()
objets=bucket.objects
print (type(objets))
print (objets.__sizeof__())
print(objets.__dict__)
print(objets.all())

print(dir(objets))
print (objets.__sizeof__())
print(objets.all())
print(dir(objets.all()))
print(objets.all().__sizeof__())
print(objets.all().__dict__)


print (objets.__len__())
iterat=objets.__iter__()
print(dir(iterat))
while iterat.__next__() :
  
  print(iterat.__next__())

# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()
# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(bucket["Name"])
"""