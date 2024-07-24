import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages, 'dates': dates})
    df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split(':\s', message)
        if len(entry) > 1:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('grp_notif')
            messages.append(entry[0] if entry else '')  # Handle empty message case

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df = df[['dates', 'user', 'message']]
    df['only_date'] = df['dates'].dt.date
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['year'] = df['dates'].dt.year
    df['day_name']=df['dates'].dt.day_name()
    df['month_num'] = df['dates'].dt.month

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df