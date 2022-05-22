# Twitter sentiment analysis

This project collects live tweets from twitter. We need to provide an authentication details for accessing such tweet data.
After accessing the tweet data, we try to find the sentiment of each tweet, by taking the help of already available text file containing sentiment score for various words / terms.
This project also tries to find the sentiment of a new term, that is not available in the text file. This is done by copmaring its frequency of occurrence and the sentiment score of the tweets.
Moreover, as an example of finding a valuable insight, this project finds the top 10 trending hashtags within the available data.
Finally, the analysis of tweets based on country of origin is also done

Below were the tasks performed:
1) "part_1_twitterstream_py3.py" file accesses live tweet data using twitter development account. You need to request for having a developer account.
2) "part_2_tweet_sentiment.py" derives the sentiment of each tweet accessed/
- A list of sentiment words was available, where number of words had a sentiment score assigned, eg. happy  +3
- This information is available in the file AFINN-111.txt
3) "part_3_term_sentiment.py" derives the sentiment of the new terms.
4) "part_4_frequency.py" computes term frequency of various words.
5) "part_5_top_ten.py" finds the top ten trending hashtags
6) "part_5_top_ten.py" - use the tweet object data for analyses. Here, I find the happiest country, based on average sentiment score of tweets.
 Here, I accessed the country of the tweet.
