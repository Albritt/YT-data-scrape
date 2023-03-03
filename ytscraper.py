
"""

This module is intended to use the Youtube data API to retrieve a playlist ID from a channel. 
After retrieving the playlist ID from channel use it to find all video IDs in playlist and use 
the video IDs to retrieve the video's statistics from the API.

"""

import os
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
import isodate

# Removed my API key for privacy, insert Google API key here
api_key = ''

api_service_name = "youtube"
api_version = "v3"

# Id of youtube channel to scrape, this is Genshin Impact's channel_id
channel_id = 'UCiS882YPwZt1NfaM0gR0D9Q'

# Get credentials and create an API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = api_key)


def get_playlist_id(youtube, channel_id):
    
    """
    Uses youtube API/key and channel_id to grab playlist ID from the given channel_id.
    """
    
    #Request data from API
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
         id=channel_id
    )
    response = request.execute()
    
    #Grab playlist ID
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
 
    return(playlist_id)

def get_playlist_video_ids(youtube, playlist_id):
   
    """
    Loops over the entire playlist one page at a time using the next_page_token to grab the video ids.
    Can only go 50 videos maximum at a time due to API constraints.
    """
    
    playlist_video_ids = []
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()
    
    for item in response['items']:
        playlist_video_ids.append(item['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    
    #While we are not at the last page
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=50,
            playlistId=playlist_id,
            pageToken = next_page_token
        )
        response = request.execute()

        #Grabbing the video id from each video
        for item in response['items']:
            playlist_video_ids.append(item['contentDetails']['videoId'])

        #Go to next page
        next_page_token = response.get('nextPageToken')
        
    
    return(playlist_video_ids)

def get_video_details(youtube, video_ids):
    
    """
    Loops over our video ids collecting the video statistics for final output to dataframe.
    """
    
    all_video_info = []
    
    #Incrementing in steps of 50 here due to API limitations
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute() 

        #Loop through our videos and grab the stats we want from the response
        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            video_info = {}
            video_info['video_id'] = video['id']

            #Put the stats of each video into our dictionary and then add dictionary to our list of all video info
            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)
    
    return pd.DataFrame(all_video_info)


playlist_id = get_playlist_id(youtube, channel_id)

video_ids = get_playlist_video_ids(youtube, playlist_id)

videos_dataframe = get_video_details(youtube, video_ids)

videos_dataframe['durationSecs'] = videos_dataframe['duration'].apply(lambda x: isodate.parse_duration(x))
videos_dataframe['durationSecs'] = videos_dataframe['durationSecs'].astype('timedelta64[s]')
videos_dataframe[['durationSecs', 'duration']] 
videos_dataframe.to_excel("stats.xlsx")




