# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:14:00 2019

@author: admin
"""

import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer

## Initialize a new API instance and get an access key
#api = landsatxplore.api.API(username, password)
#
## Perform a request. Results are returned in a dictionnary
#response = api.request('<request_code>', parameter1=value1, parameter2=value2)
#
## Log out
#api.logout()
#import landsatxplore.api

# Initialize a new API instance and get an access key
api = landsatxplore.api.API('username', 'password')

# Request
scenes = api.search(
    dataset='LANDSAT_ETM_C1',
    latitude=19.53,
    longitude=-1.53,
    start_date='1995-01-01',
    end_date='1997-01-01',
    max_cloud_cover=10)

print('{} scenes found.'.format(len(scenes)))

for scene in scenes:
    print(scene['acquisitionDate'])

api.logout()



ee = EarthExplorer('username', 'password')

ee.download(scene_id='LT51960471995178MPS00', output_dir='./data')

ee.logout()