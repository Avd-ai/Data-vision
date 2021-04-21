import sys 
import json

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
def get_hashtags(raw_file):   
    i =0
    hashtag_list = []
    for raw_tweet in raw_file:            # one iteration per an individual tweet
        x=len(raw_tweet)                # this length shows if the tweet is deleted or not. 
                                  # If x = 1, then its deleted. Else it has many fields.
        if x== 1:          #means if the tweet is deleted.  So skip the rest of iteration.
            continue

        #print(x)
        hashtag_field = raw_tweet['entities']['hashtags']
                #This gives a list of information chunks for each hashtag. If 4 hashtags are present
                #in a tweet, the list will contain 4 elemnts, each of which is a dicitonary in itself.

        if len(hashtag_field) == 0 :   # means no hashtag was used
            continue
        else:
            for element in hashtag_field:   #the dictionary for each hashtag has 2 keys-'text','indices'
                actual_hashtag = element['text']    # The value of 'text' is the actual hashtag
                #print(actual_hashtag)
                i += 1       # to keep count of all hashtags in total
                hashtag_list.append(actual_hashtag)     # putting all the hashtags in one list

    return hashtag_list

def count_hashtag_freq(raw_hash_list):
    freq_dict = {}
    for hashtag in raw_hash_list:
        if hashtag in freq_dict:       # means, the hashtag is already entered in dictionary, and we 
            freq_dict[hashtag] += 1     # just need to increase the count by 1
        else:
            freq_dict[hashtag] = 1    # add the hashtag in dict, with value/count as 1
    return(freq_dict)

def find_top(freq_dict, num):
    ordered_dict = dict(sorted(freq_dict.items(), key=lambda item:item[1], reverse=True))
        # reference: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    #print(ordered_dict)

    # to direct print the required output
    i = 0
    for hashtag in sorted(ordered_dict, key=ordered_dict.get, reverse=True):
        if i<num:
            print(hashtag, ordered_dict[hashtag])
            i += 1
        else:
            break    # so that only top ten hashtags are printed

def main():
    converted_file = convert_from_json()

    hashtag_list =get_hashtags(converted_file)
    #print(hashtag_list)

    freq_dict = count_hashtag_freq(hashtag_list)

    find_top(freq_dict,10)      # can change the number, if we want, say top 100, hashtags

if __name__ == '__main__':

    main()