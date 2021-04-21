import sys 
import json

''' This file is to be run from terminal using the command:
python happiest_state.py AFINN-111.txt output.txt

Becuase, the tweet  data has country codes, rather than state codes, and as tweets are from 
 all over the world, I have showed the happiest country instead
'''

# FUNCTION TO CONVERT AFINN TEXT FILE INTO A DESIRED DICTIONARY FORMAT
def Afinn_to_dict():
    a_file = open('AFINN-111.txt') # OR
    #a_file = open(sys.argv[1])
    senti_dict ={}

    for line in a_file:
        word_or_phrase, senti_score = line.split(sep = '\t')
        senti_dict[word_or_phrase] = senti_score

    #print(len(senti_dict))
    return senti_dict

# actually tweet file related conversion: TO CONVERT FROM JSON TO PYTHON FORMAT
def tweets_json_to_dict():
    a_list=[]
    a_file = open(sys.argv[2])
    #a_file = open('output.txt')

    for line in a_file:
        py_object = json.loads(line)
        a_list.append(py_object)
    #above thing created a list of dicitonaries converted from json file of tweets.
    # THat is, each element of a list, which is itself a dicitonary, represents one tweet.

    #for item in a_list[35]:
        #print(item, '\t', a_list[35][item])     # this gave error because this tweet is deleted

    return a_list

# TO EXTRACT THE TEXT FROM TWEET AND FIND ITS SENTIMENT SCORE
def extract_text_and_score(indivi_tweet,senti_dict):
    score = 0
    actual_text = indivi_tweet['text']     # Retrieve the actual text of the tweet.
    splitted_text = actual_text.split()    # split into a list of words, 
                                                    #for comparison with scored terms
    for word_in_sentence in splitted_text:          # check every word in a tweet, with
        for senti_term in senti_dict:         # every word in the sentiment dictionary
            if word_in_sentence == senti_term:
                score = score + int(senti_dict[senti_term])
    return score

# TO RETRIEVE THE COUNTRY CODE AND ADD THE SCORE RESPECTIVELY
def get_location(list_of_raw_tweets, senti_dict):
    cnt =0
    country_dict ={}
    for tweet in list_of_raw_tweets:
        if len(tweet) == 1:          # that is, the tweet is deleted
            continue       
        else:
            if tweet['place'] is not None:       # that is, if the tweet has details about location
                tweet_score = extract_text_and_score(tweet, senti_dict)
                # print(tweet_score)        # it can be seen that, among the few tweets, most are neutral

                #print(tweet['place']['country'])
                country_of_tweet = tweet['place']['country_code']
                if country_of_tweet not in country_dict:
                    country_dict[country_of_tweet] = tweet_score   # adding score every time
                else:
                    country_dict[country_of_tweet] += tweet_score
                cnt += 1
    print(f'Only {cnt} tweets have "place" value mentioned')
    print('All the countries with available net sentiment score are as below: ',country_dict)
    return country_dict
    


def main():

    senti_dictionary = Afinn_to_dict()    # function to convert available sentiment score file into 
                                        #  a dictionary
    list_of_tweets = tweets_json_to_dict() 

    dict_with_ctr_scores = get_location(list_of_tweets, senti_dictionary)

    # Following code is for finding the happiest country
    i = 0
    num = 1     # to find only the topmost happy country
    for country in sorted(dict_with_ctr_scores, key=dict_with_ctr_scores.get, reverse=True):
        if i<num:
            #print(country, dict_with_ctr_scores[country])
            i += 1
            print(f'\n{country} is the happiest state/country with score {dict_with_ctr_scores[country]}')
        else:
            break  


if __name__ == '__main__':
    main()