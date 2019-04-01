#! /usr/bin/python
#coding: utf8
import requests
#url="http://api.planetos.com/v1/datasets/noaa_gfs_pgrb2_global_forecast_recompute_0.25degree/point?start=2019-03-31T18:00:00Z&end=2019-03-31T18:00:00Z&lat=50.7&lon=3.06&z=all&var=ugrd_m,vgrd_m&count=100&apikey=c96235b15d0d4188905993f8d7ea3daa"
url="http://api.planetos.com/v1/datasets/noaa_gfs_pgrb2_global_forecast_recompute_0.25degree"

querystring = {"lon":3.06,
                "lat":50.7,
                "z":"all",
                "var":"ugrd_m",
                "start":"2019-03-31T18:00:00Z",
                "end":  "2019-03-31T18:00:00Z",
                "count":"100",
                "apikey":"c96235b15d0d4188905993f8d7ea3daa"}

response = requests.request("GET", url, params=querystring)
#response = requests.request("GET", url)
print(response.text)

"""
ugrd_m
u-component of wind @ Specified height level above ground
vgrd_m
v-component of wind @ Specified height level above ground

"https://api.planetos.com/v1/datasets/noaa_gfs_pgrb2_global_forecast_recompute_0.25degree/point?origin=dataset-details&lat=49.5&apikey=c96235b15d0d4188905993f8d7ea3daa&lon=-50.5&_ga=2.144265141.1021343701.1554030753-260602376.1554030753"
#http://api.planetos.com/v1/datasets/noaa_gfs_pgrb2_global_forecast_recompute_0.25degree/point?var=Temperature_surface&lat=50.7&lon=3.06&apikey=c96235b15d0d4188905993f8d7ea3daa
"""