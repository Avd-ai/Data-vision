import sys 
import json

'''
ALGORITHM:
1) Convert AFINN into dictionary format, and tweet file into python format
2) retrieve actual text data
3) find total  occurence of terms from AFINN in whole tweet file.
    This number will help how much threshold we should put for deciding the correlation between the
    new term and a sentiment. Eg. if 1200 occurences of known sentiment words, then we can put 
    threshold that, if 1200/100 = 12 times a word co-occurs along with any of the positive words 
    collectively, or with the negative words collectively, (whicheve is more, in  case it co-occurs with
    both negative and positive words more than 12 times), we can say that the new word also carries 
    the same sentiment.
4) get only that part dictionary, which occurs in the tweet file. Un-occurred terms from AFINN are
    filtered. It will reduce the number of iterations later on.
5) decide threshold. Total/100 in this case.
6) find sentiment of a new word: Create a new empty dictionary for new words.
    Whenever a term from AFINN occurs, put all other words in that tweet in the new dictionary, and 
    mention if it has positive sentiment or negative, based on the AFINN term.
    This is done by creating a list for every new such word/term, where first element of list represents
    number of occurences of that word along with a positive term. Second element is a number of 
    occurence along with a negative term.
7) Filter only those new words, whose count of either positive or negative is more than the threshold.
8) print new word with its sentiment
'''
def Afinn_to_dict():
    a_file = open('AFINN-111.txt')

    senti_dict ={}

    for line in a_file:        
        word_or_phrase, senti_score = line.split(sep = '\t')
        senti_dict[word_or_phrase] = senti_score
    return senti_dict

def tweets_json_to_dict():
    a_list=[]

    a_file = open(sys.argv[2])
    #a_file = open('output.txt')

    for line in a_file:
        py_object = json.loads(line)
        a_list.append(py_object)
    return a_list

def get_actual_text(raw_file):   
    actual_tweet_list = []
    for raw_tweet in raw_file:            # one iteration per an individual tweet
        x=len(raw_tweet)                # this length shows if the tweet is deleted or not. 
        #print(x)                  # If x = 1, then its deleted. Else it has many fields.
        
        if x== 1:          #means if the tweet is deleted.  So skip the rest of iteration.
            continue
        
        actual_text = raw_tweet['text']     # Retrieve the actual text of the tweet.
        splitted_text = actual_text.split()  # gives a list of words for an individual tweet
        
        actual_tweet_list.append(splitted_text)

    return actual_tweet_list

def calc_total_senti_words(tweet_word_list, senti_dict):
    
    new_term_freq_dict ={}
    for tweet in tweet_word_list:
        for word in tweet:
            if word in senti_dict.keys():
                if word in new_term_freq_dict:
                    new_term_freq_dict[word] += 1
                else:
                    new_term_freq_dict[word] = 1
            else:
                continue
    #print(new_term_freq_dict)

    # now add the whole frequency of each senti term
    total = 0
    for key in new_term_freq_dict:
        total += new_term_freq_dict[key] 
    return total, new_term_freq_dict


def find_new_senti_words(actual_text_list, senti_dict,relevant_dict):
    new_senti_dict = {}

    for rele_term in relevant_dict.keys():
        for tweet in actual_text_list:
            if rele_term in tweet:
                for word in tweet:
                    if word != rele_term:
                        if word in new_senti_dict.keys():
                            if int(senti_dict[rele_term]) >0 :  # means positive
                                new_senti_dict[word][0] += 1
                            else:
                                new_senti_dict[word][1] += 1  # means adding for negative senti count
                            
                        else:       #means word is not alredy in new_senti_dict
                            new_senti_dict[word] = [0,0]
                            if int(senti_dict[rele_term]) > 0:
                                new_senti_dict[word][0] += 1
                            else: 
                                new_senti_dict[word][1] += 1
                    else:
                        continue
            else:
                continue
    return (new_senti_dict)        # this resulting  dictionary  is a collection of all the words that 
        # have at least one sentiment word in the tweet the belong to.
        # For each such tweet that they are part of, they also receive one count  for either positive/negative
        # senti word that they accompany. This is availabel in the form of list of 2, attached to the word.
        # First number in this list is for the co-occurence of positive words, second number is for
        # negative words 

def filter_for_threshold(new_senti_dict, threshold):
    final_dict = {}
    for item in new_senti_dict:
        if new_senti_dict[item][0] >= threshold:
            if new_senti_dict[item][0] > new_senti_dict[item][1]:
                final_dict[item] = ['+ve', new_senti_dict[item][0]]
            else:
                final_dict[item] = ['-ve', new_senti_dict[item][1]]
        elif new_senti_dict[item][1] >= threshold:
            final_dict[item]= ['-ve', new_senti_dict[item][1]]
    return(final_dict)

def main():
    senti_dict = Afinn_to_dict()

    list_of_tweets = tweets_json_to_dict()

    actual_text_list = get_actual_text(list_of_tweets)
    
    total, relevant_dict  = calc_total_senti_words(actual_text_list, senti_dict)
    print(total)
    
    threshold = total/100    # need to change the divisor based on the size of the dataset
            # bigger the divisor, more number of new senti words we get.
            # threshold is minimun number of co-occurence a new term should have with already
                # scored terms

    new_senti_dict = find_new_senti_words(actual_text_list, senti_dict, relevant_dict)
    
    final_dict = filter_for_threshold(new_senti_dict, threshold)

    for new_term in final_dict:
        print(new_term, ' ', final_dict[new_term][0])



if __name__ == '__main__':
    main()
