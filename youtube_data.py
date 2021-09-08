# Author:  Jake Lovrin
# HW3
# I pledge my honor that I have abided by the Stevens Honor System. -Jake Lovrin

#  youtube_data.py searches YouTube for videos matching a search term

# To run from terminal window:   python3 youtube_data.py 

from apiclient.discovery import build      # use build function to create a service object

import unidecode   #  need for processing text fields in the search results
import csv         # used to read/write to a .csv file

# put your API key into the API_KEY field below, in quotes
API_KEY = ""

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

#  function youtube_search retrieves the YouTube records

def youtube_search(s_term, s_max):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(q=s_term, part="id,snippet", maxResults=s_max).execute()
    
    # print the search term, search max
    print(search_term)
    print(search_max)
    print("")

    # manage CSV interactions and define headlines
    CSVFile = open('results.csv', 'w')
    CSVWriter = csv.writer(CSVFile)
    CSVWriter.writerow(["Title", "Id", "Views", "Likes", "Dislikes", "Comments", "Like Ratio", "Dislike Ratio"])

    # Setting up some values for data analysis
    all_items = []
    highest_views = []          # Top 5 Highest View Count
    highest_like_ratio = []     # Top 5 Highest Like Percentage Likes/Views
    highest_dislike_ratio = []  # Top 5 Highest Dislike Percentage Dislikes/Views

    # search for videos matching search term;    
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  
            videoId = search_result["id"]["videoId"]
            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            for video_results in video_response.get("items",[]):
                viewCount = video_results["statistics"]["viewCount"]
                if 'likeCount' not in video_results["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_results["statistics"]["likeCount"]
                if 'dislikeCount' not in video_results["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_results["statistics"]["dislikeCount"]
                if 'commentCount' not in video_results["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_results["statistics"]["commentCount"]
            
            print("")    
            print(title,videoId,viewCount,likeCount,dislikeCount,commentCount)
            like_percent = int(likeCount)/int(viewCount)
            dislike_percent = int(dislikeCount)/int(viewCount)
            viewCount = int(viewCount)
            CSVWriter.writerow([title, videoId, viewCount, likeCount, dislikeCount, commentCount, like_percent, dislike_percent])
            all_items.append([title, videoId, viewCount, likeCount, dislikeCount, commentCount, like_percent, dislike_percent])

    # Flush a line in the CSV, write in the list we just created, then print the same thing to the console
    CSVWriter.writerow("")
    CSVWriter.writerow(all_items)
    print(all_items)

    # Rinse and repeat for view
    highest_views = sorted(all_items, key=lambda x: x[2], reverse=True)
    print("")
    print("Highest Views")
    #print(highest_views[:5])
    
    # Loop through for a prettier printing
    count_views = 1
    for entry in highest_views:
        if count_views > 5:
            break
        print(str(count_views) + ". " + str(entry[:3]))
        count_views += 1

    CSVWriter.writerow("")
    CSVWriter.writerow(["Highest Views"])
    # Set up the same loop for writing to the CSV
    count_views = 1
    for entry in highest_views:
        if count_views > 5:
            break
        row_input = str(count_views) + ". " + str(entry[:3])
        CSVWriter.writerow([row_input])
        count_views += 1

    # Then the like ratio
    highest_like_ratio = sorted(all_items, key=lambda x: x[6], reverse=True) #Had some weird sorting issues, so the list being reversed solved some problems
    print("")
    print("Highest Like to View Ratio")
    
    count_views = 1
    for entry in highest_like_ratio:
        if count_views > 5:
            break
        print(str(count_views) + ". " + str(entry[:2]) + str(entry[-1]))
        count_views += 1

    CSVWriter.writerow("")
    CSVWriter.writerow(["Highest Like to View Ratio"])

    count_views = 1
    for entry in highest_like_ratio:
        if count_views > 5:
            break
        row_input = str(count_views) + ". " + str(entry[:2]) + str(entry[-2])
        CSVWriter.writerow([row_input])
        count_views += 1
    #CSVWriter.writerow(highest_like_ratio)

    # And the dislike ratio
    highest_dislike_ratio = sorted(all_items, key=lambda x: x[7], reverse=True)
    print("")
    print("Highest Dislike to View Ratio")
    
    count_views = 1
    for entry in highest_dislike_ratio:
        if count_views > 5:
            break
        print(str(count_views) + ". " + str(entry[:2]) + str(entry[-1]))
        count_views += 1

    CSVWriter.writerow("")
    CSVWriter.writerow(["Highest Dislike to View Ratio"])

    count_views = 1
    for entry in highest_dislike_ratio:
        if count_views > 5:
            break
        row_input = str(count_views) + ". " + str(entry[:2]) + str(entry[-1])
        CSVWriter.writerow([row_input])
        count_views += 1

    CSVFile.close()
    

# main routine

print("Please enter your search term here:")
search_term = input() # define term here
print("Please enter a max number of searches(at least 5):")
search_max = input() # define maximum here
    
youtube_search(search_term, search_max)
