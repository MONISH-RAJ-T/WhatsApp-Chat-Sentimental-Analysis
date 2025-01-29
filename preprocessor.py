import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')

def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s[a|p]?m?\s?-\s'
    messages = re.split(pattern, data, flags=re.I)[1:]
    dates = re.findall(pattern, data, flags=re.I)

    dates1= []
    for lst in range(len(dates)):
      dte = dates[lst].split('-')[0].strip()
      dates1.append(dte)

    df = pd.DataFrame({'user_message':messages,'message_date':dates1})
    df['message_date'] = pd.to_datetime(df['message_date'], infer_datetime_format=True)
    df.rename(columns={'message_date':'date'},inplace=True)
    
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(':', message)
        if entry[1:]:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df = df[df['user'] != 'group_notification']

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    def remove_punctuation(word):
        word_list = word_tokenize(word)
        lst = []
        for i in word_list:
            if i not in string.punctuation:
                lst.append(i)

        return ' '.join(lst)

    df['message'] = df['message'].apply(remove_punctuation)

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df
