import sys
import json
import decimal      # to specify the number of decimals

'''This file is to be run as "python frequency.py tweet_file_name("output" in this case).txt"
'''
# ALGORITHM:
# 1) Retrieve actual 'text' of every tweet. May be create a list of all the texts
# 2) Convert every text into a list of words. Easier to compare every word
# 3) Create an empty dictinary. (Elements should be 'terms as keys', and 'frequencies as values')
# 4) Fill the dictionary: parse every tweet, and add every new word to the dictionary, and give count as 1.
#   When the word is already present, add the count by one.
# 5) Count the total number of words in whole file, by calculating number of words in all computed lists,
    # or by adding the frequency of all the terms in the built dictionary.
# 6) create a new dictionary (or can modify the existing one as well). Take every key, and calculate
    # value as existing value / total number of terms
# 7) Can convert into a dataframe, and then print the ouptut.

def lines(fp):
    print ('Number of tweets is: ',str(len(fp.readlines())))

#to convert tweet data from  json to python format
def convert_from_json():
    a_list=[]
    a_file = open(sys.argv[1])

    #Created a list of every line in the tweet_data file. So, each element is a tweet in its raw form
    for line in a_file:
        py_object = json.loads(line)
        a_list.append(py_object)
    #print(len(a_list), 'inside json conversion')
    return a_list

# from all raw data, we extract actual text of the tweet
def get_actual_text(raw_file):   
    i =0
    actual_tweet_list = []
    for raw_tweet in raw_file:            # one iteration per an individual tweet
        x=len(raw_tweet)                # this length shows if the tweet is deleted or not. 
        #print(x)                  # If x = 1, then its deleted. Else it has many fields.
        
        if x== 1:          #means if the tweet is deleted.  So skip the rest of iteration.
            continue
        
        actual_text = raw_tweet['text']     # Retrieve the actual text of the tweet.
        i += 1
        #print('tweet number ', i)
        #print(actual_text)
        splitted_text = actual_text.split()  # gives a list of words for an individual tweet
        
        actual_tweet_list.append(splitted_text)    # adding the new list of words as an element into
                            # the bigger list of all tweets

    # Result will be bigger_list_of_all_tweets = [[word_list_of_tweet_1], [word_list_of_2], ...]
    #print(actual_tweet_list)
   
    return actual_tweet_list

def create_fill_dict(tweet_list_of_words):
    dict_of_terms = {}
    for tweet in tweet_list_of_words:
        for word in tweet:

        #first check if the word is already present in the dicitonary
            if word in dict_of_terms:
                dict_of_terms[word] += 1       # adding the count by one
        
        # if the word is not present, add the word, and value as 1
            else:
                dict_of_terms[word] = 1       
    
    return dict_of_terms
 

def calc_total_words(tweet_word_list, dict_with_freq):
    
    # Two ways to count total number of words. One from the list of tweet texts, another from
            # adding frequencies of each term. Both should give same result.
    list_count = 0
    dict_cnt = 0

    for tweet in tweet_word_list:
        list_count +=  len(tweet)
    #print('Total number of words from list_cnt is: ',list_count)

    for term in dict_with_freq:
        dict_cnt += dict_with_freq[term]
    #print('total of all frequencies from dict is: ', dict_cnt)

    return dict_cnt

def desired_form_conversion(dict_with_freq, total_freq):
    
   # print in the desired format - each term and its frequency on the new line
    for term in dict_with_freq:
        #dict_with_freq[term] = dict_with_freq[term] / total_freq   # ideal code

        # but we will round the fraction upto 4 places after decimal
        dict_with_freq[term] = round(dict_with_freq[term] / total_freq, 6)  
    #print(dict_with_freq)
    return dict_with_freq

def main():
    tweet_file = open(sys.argv[1])
    lines(tweet_file)

    # function to retrieve the actual text of the tweet
    converted_file = convert_from_json()
    # converted_file is a list of tweets that is still in raw format.
     # every element of the list is an individual tweet, which in itself,can be a dictionary or a list.

    tweet_text_list = get_actual_text(converted_file)
    # The received list is a list of only text part of each tweet

    #print(len(tweet_text_list),'is length of nested list, after removing the deleted tweets')
    #print(tweet_text_list)

    complete_dict_freq = create_fill_dict(tweet_text_list)
    # The receivved thing is a dictionary with frequency of each term
    #print(complete_dict_freq)

    #for term in complete_dict_freq:
       # print(term,'\t',complete_dict_freq[term])   #prints every term with its frequency on new line

    #  Now we will calculate the total number of words in the document
    total_freq = calc_total_words(tweet_text_list, complete_dict_freq)

    # to convert frequency into  proportional fractions
    desired_dict = desired_form_conversion(complete_dict_freq, total_freq)

    #print the final required output - each term on a new line
    for term in desired_dict:
        1+1             # just to have some operation in the loop, in case we comment the next line
                                # (to prevent the long output in the console)
        print(term, ' ', desired_dict[term])
    ''' THE CODE LINE ABOVE IS THE MOST IMPORTANT, WHICH GIVES THE DESIRED OUTPUT.
        FOR THE SAKE OF AVOIDING VERY LONG OUTPUT IN THE CONSOLE IT MIGHT BE TEMPORARILY COMMENTED'''

if __name__ == '__main__':
    main()
