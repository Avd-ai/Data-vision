''' This file is to be used from terminal. And that would be in format as below:
#   python tweet_sentiment.py Afinn-111.txt problem_1_submission.txt
 Here, Afinn is file name consisting of scores for variuos words, and 
   problem_1_submission.txt is the file full of tweets retrieved from the twitter site

 In similar fashion, we can type "python tweet_sentiment.py Afinn-111.txt output.txt" as well.
'''


''' This file can give output in two ways:
a) Each score one after another, on the next line, soon after calculating the score. 
This happens in the dedicated function 'COUNTING_SENTI_SCORE' 
(This has been commented as of now, for the ease of viewing the output - line 127)
b) List of scores, which is returned to the 'main' function.
'''
import sys 
#import pandas as pd
import json

# dummy trial function, which counts the number of elements of file name entered at the console
def lines(fp):
    print (str(len(fp.readlines())))

def Afinn_to_dict():
    a_file = open('AFINN-111.txt')
    # or a_file = open(sys.argv[1])

    senti_dict ={}
    for line in a_file:
        #print(i)
        
        word_or_phrase, senti_score = line.split(sep = '\t')
        senti_dict[word_or_phrase] = senti_score
    #print(senti_dict)
    #print(len(senti_dict))
    return senti_dict

# actually tweet file related conversion:
def tweets_json_to_dict():
    a_list=[]

    a_file = open(sys.argv[2])
    #a_file = open('output.txt')

    for line in a_file:
        py_object = json.loads(line)
        a_list.append(py_object)
    
    #above thing created a list of dicitonaries converted from json file of tweets.
    # THat is, each element of a list, which is itself a dicitonary, represents one tweet.

    # below 3 lines can help understand the nature of a tweet
    '''print(a_list[0])
    print(type(a_list[0]))
    print(len(a_list))
    '''
    return a_list

# to look at an individual tweet in formatted form;   This is to test and understand the structure of data.
def details_of_tweet(list_of_raw_tweets):

    # take any random tweet by index, and see its details by putting that index in below lines
    
    print('length of this dictionary tweet is : ',len(list_of_raw_tweets[9]))
                            # prints total items in a tweet, which is a dictionary in itself

    for item in list_of_raw_tweets[0]:
        print(item, '\t', type(list_of_raw_tweets[0][item])) # each field of an individual tweet
        
        if (item != 'delete'):
            if ((type(list_of_raw_tweets[0][item]) == str)or
                                (type(list_of_raw_tweets[9][item]) == dict)):
                print(len(list_of_raw_tweets[9][item]))
                    # above line works only if the tweet is not deleted.

        else:
            print('The tweet was deleted.') 
            print('Most of the info about the tweet is not more available.\n')
        
        #print(list_of_raw_tweets[9][item])       # prints the value of each field (not the key)
    #print('\n',list_of_raw_tweets[9]['text'])      # printing actual text
    
    # printing the whole tweet, without any formatting
    #print(list_of_tweets[9])


def counting_senti_score(word_dictionary, list_of_raw_tweets):
    
    score_list_of_tweets = []
    # three counters below show larger picture of how many tweets had what overall nature/sentiment.
    counter_of_positive_tweets = 0
    counter_of_negative_tweets = 0
    neutral_tweet_count = 0
    deleted_tweets = 0

    for tweet in list_of_raw_tweets:            # one iteration per an individual tweet
        score = 0
        x=len(tweet)                # this length shows if the tweet is deleted or not. 
                                # If x = 1, then its deleted. Else it has many fields.
        #print(x)

        if x== 1:          #means if the tweet is deleted.  So skip the rest of iteration.
            score_list_of_tweets.append(0)  # putting score 0 for deleted tweets
            deleted_tweets += 1
            continue
        
        actual_text = tweet['text']     # Retrieve the actual text of the tweet.
        #print(actual_text)
        splitted_text = actual_text.split(" ")    # split into a list of words, 
                                                    #for comparison with scored terms
        # print(splitted_text)

        for word_in_sentence in splitted_text:          # check every word in a tweet, with
            for senti_term in word_dictionary:          # every word in the sentiment dictionary
                if word_in_sentence == senti_term:
                    score = score + int(word_dictionary[senti_term])        # add the respective score
        
        # ***********  IMP ************
        ''' THE LINE BELOW IS THE ONE THAT GIVES THE REQUIRED OUTPUT, 
                THAT IS THE SENTIMENT SCORE OF EACH TWEET'''
        print(score)       # this might be commented for avoiding long output in the console

        # *********** IMP *************

        if score > 0:
            counter_of_positive_tweets += 1
        elif score < 0:
            counter_of_negative_tweets += 1
        else:
            neutral_tweet_count += 1
        score_list_of_tweets.append(score)
    print('number of positive tweets: ', counter_of_positive_tweets)
    print('number of negative tweets: ', counter_of_negative_tweets)
    print('number of neutral tweets: ', neutral_tweet_count)
    print('number of deleted tweets: ', deleted_tweets)
    return (score_list_of_tweets)

'''for tweet in list_of_tweets:     # 'tweet' here gives only the key, and not the whole item
        actual_text = tweet['text']
        print(actual_text)  
    return 3    '''     #Why these 3 lines not working?--> 
                #because deleted tweets don't have 'text' field

def main():
    import json

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #lines(sent_file)
    lines(tweet_file)
    print('Above number is the total number of tweets in the original file with raw data.')

    senti_dictionary = Afinn_to_dict()    # function to convert available sentiment score file into 
                                        #  a dictionary

    list_of_tweets = tweets_json_to_dict()   # function to convert tweets into
                                                    # python data structure format

    #details_of_tweet(list_of_tweets)     # this function is for testing only.
    
    #Function below is for actual calculation of score for each tweet
    final_tweet_score_list = counting_senti_score(senti_dictionary, list_of_tweets)
        # It returns the list of scores for every tweet
    
    print('The count of scored tweets: ', len(final_tweet_score_list))  # to verify that every tweet has been scored.

    # print('Following is list of scores for each tweet: \n',final_tweet_score_list)   # prints in list format



if __name__ == '__main__':

    main()
