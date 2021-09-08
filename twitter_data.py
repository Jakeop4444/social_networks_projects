# twitter_data.py searches Twitter for tweets matching a search term,
#      up to a maximun number

######  user must supply authentication keys where indicated

# to run from terminal window: 
#        python3  twitter_data.py   --search_term  mysearch   --search_max  mymaxresults 
# where:  mysearch is the term the user wants to search for;  default = music
#   and:  mymaxresults is the maximum number of results;  default = 30

# other options used in the search:  lang = "en"  (English language tweets)
#  and  result_type = "popular"  (asks for most popular rather than most recent tweets)

# The program uses the TextBlob sentiment property to analyze the tweet for:
#  polarity (range -1 to 1)  and  
#  subjectivity (range 0 to 1 where 0 is objective and 1 is subjective)

# The program creates a .csv output file with a line for each tweet
#    including tweet data items and the sentiment information

from textblob import TextBlob	# needed to analyze text for sentiment
import argparse    				# for parsing the arguments in the command line
import csv						# for creating output .csv file
import tweepy					# Python twitter API package
import unidecode				# for processing text fields in the search results
import html                     # ^
import string                   # ^

CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

def clean(text):
    try:
        return ''.join(list(filter(lambda ch: ch in set(string.printable), html.unescape(text)))).replace('\n','')
    except:
        return text

def analyze_single_tweet(tweet):
    data = []                               #Create array to store data

    data.append(tweet.created_at)           #Date created
    data.append(tweet.text)                 #Text of the tweet
    data.append(tweet.retweet_count)        #Number of retweets	
    data.append(tweet.user.name)            #Username
    data.append(tweet.user.id)           	#User ID
    data.append(tweet.user.followers_count) #Number of user followers
    data.append(tweet.user.friends_count)   #Number of user friends

    #Use TextBlob to determine polarity and subjectivity of tweet
    text_blob = TextBlob(tweet.text)

    data.append(text_blob.polarity)
    data.append(text_blob.subjectivity)

    #Format text for all fields so they can be written to CSV
    data = list(map(clean, data))

    return data

def analyze_term(api, term, search_max, file_name):
    #Store total polarity metric to find polarity of overall term
    total_polarity = 0

    #Store all tweets polarities to find standard deviation after the mean is found
    tweet_polarities = []

    #Total amount of tweets
    amt_tweets = 0

    #Create a .csv file to hold the results, and write the header line
    with open(file_name, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["username","userid","created", "text", "retweets", "followers",
            "friends","polarity","subjectivity"])

        #Do the twitter search
        for tweet in tweepy.Cursor(api.search, q=term, lang="en", result_type = "popular").items(search_max):
            #Get information on one tweet
            data = analyze_single_tweet(tweet)

            #Grab polarity from the tweet
            tweet_polarity = data[-2]
            
            #Sum polarity to find the mean
            total_polarity += tweet_polarity

            #Add this tweets polarity to array for Standard deviation later
            tweet_polarities.append(tweet_polarity)

            # write tweet info to .csv tile
            csvWriter.writerow(data)

            amt_tweets += 1
    
    #Statistical Analysis
    avg_polarity = total_polarity / amt_tweets
    standard_deviation = ((sum(list(map(lambda val: (val - avg_polarity) ** 2, tweet_polarities)))) / (amt_tweets - 1)) ** 0.5

    #Return the statistics
    return avg_polarity, standard_deviation

def twitter_analysis(search1, search2, search_max):
    #AUTHENTICATION (OAuth)
    authenticate = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(authenticate)

    #Analyze Twitter for the first term
    term1_mean, term1_sd = analyze_term(api, search1, search_max, 'twitter_search1_results.csv')    

    #Do the same, for the second term
    term2_mean, term2_sd = analyze_term(api, search2, search_max, 'twitter_search2_results.csv')

    print('Average polarity for term {0}: {1:0.2f}'.format(search1, term1_mean))
    print('Average polarity for term {0}: {1:0.2f}'.format(search2, term2_mean))

    more_polarized = search1 if term1_sd > term2_sd else search2
    highersd = term1_sd if term1_sd > term2_sd else term2_sd
    lowersd = term1_sd if term2_sd > term1_sd else term2_sd
    print('Term {0} is more polarized, with standard deviation {1:.2f} vs. {2:.2f}'.format(more_polarized, highersd, lowersd))

def main():
    #Get the input arguments - search_term1, search_term2, and search_max
    parser = argparse.ArgumentParser(description='Twitter Search')
    parser.add_argument("--search_term1", action='store', dest='search_term1', default="puppies")
    parser.add_argument("--search_term2", action='store', dest='search_term2', default="kittens")
    parser.add_argument("--search_max", action='store', dest='search_max', default=30)
    args = parser.parse_args()

    search1 = args.search_term1
    search2 = args.search_term2
    search_max = int(args.search_max)

    if search1 == 'puppies' and search2 == 'kittens':
        print('Running with default arguments for terms')
        print('You can run with custom arguments using --search_term1 <TERM> and --search_term2 <TERM>')
        print()

    if search_max == 30:
        print('Running with default arguments for amount')
        print('You can run with custom arguments using --search_max <AMOUNT>')
        print()

    print('Term 1: {0}'.format(search1))
    print('Term 2: {0}'.format(search2))
    print('Maximum Amount: {0}'.format(search_max))

    twitter_analysis(search1, search2, search_max)

if __name__ == '__main__':
    main()