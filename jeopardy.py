#%% imports and init
import pandas as pd
import datetime
import re

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data = pd.read_csv('jeopardy.csv')

#%%Cleaning
#### Cleaning the Dataset
# print(data.columns)

formatted_columns = {
    'Show Number': 'show_number',
    ' Air Date': 'air_date',
    ' Round': 'round',
    ' Category': 'category',
    ' Value': 'value',
    ' Question': 'question',
    ' Answer': 'answer',
    }

data.rename(columns=formatted_columns, inplace=True)

## Convert value column in number format
data['value'].replace('None', 0, inplace=True)
data['value'] = data['value'].replace('[$,]', '', regex=True).astype(float)

## Convert the date into datetime
data['year'] = data['air_date'].apply(
    lambda date: datetime.datetime.strptime(date, '%Y-%m-%d').year
    )

print(data.dtypes)


#%% Get all questions in a particular list
words_to_find = ['Computer']

# The Reggex here makes it relatively slow
# TODO: Find more efficient way to parse throught the questions

def get_questions_with_words(data, word_lst):
    find_words = lambda question: \
        all([re.search("(^|\W){}\W".format(word.lower()), question.lower()) \
             for word in words_to_find])
    
    return data.loc[data['question'].apply(find_words)]
               
filtered_questions = get_questions_with_words(data, words_to_find)

print("Found {} questions with the words {}"\
      .format(len(filtered_questions), words_to_find))
print("The mean score for these questions is {}" \
      .format(filtered_questions.value.mean()))

def get_unique_answer_count(filtered_questions):
    return filtered_questions['answer'].value_counts()

print("\nThe top 10 unique answers for all questions containing the words {}\
 are:\n{}" \
    .format(words_to_find, get_unique_answer_count(filtered_questions)[:10]))

#%% Look at how the questions change over time
#Basically take the filtered questions and look at their numbers through time

def group_by_year(filtered_questions):
    grouped_questions = filtered_questions.groupby('year')\
        .question\
        .count()\
        .reset_index(name="appearances")\
        .sort_values('appearances', ascending=False)
    
    return grouped_questions

print(group_by_year(filtered_questions))


#%% Look at the potential connection between rounds and categories

def filter_category_by_round(data, category):
    category_data = data.loc[data['category'] == category.upper()]
    
    grouped_data = category_data.groupby(['category', 'round'])\
        .question.count()\
        .reset_index(name="Apperances")
        
    return grouped_data
        
print(filter_category_by_round(data, '"A" IN SCIENCE'))


































