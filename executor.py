import pandas as pd
import gspread
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = api_id
api_hash = 'api_hash'
string_session = str("telegram_string_token")

old_history = pd.read_csv('history.csv', index_col=0)

client = TelegramClient(StringSession(string_session), api_id, api_hash)
client.start()

# with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
all_messages = []
for i in client.get_messages('w9ME0Iixm9mMDMy', limit=100):
    if i.message is not None and '[bot]' not in i.message:
        all_messages.append([i.id, i.date.strftime("%-m/%-d/%Y %H:%M:%S"), i.message])

history = pd.DataFrame(all_messages, columns=['id', 'dt', 'message'])
# print(history)
new_history = history[history.id.isin(old_history.id)==False].copy()
# new_history = history.copy()
new_history['message_parsed'] = new_history['message'].apply(lambda x: x.split('\n'))

def is_valid(list_):
    if len(list_) >= 2 and len(list_) <= 3:
        is_valid_ = True
    else:
        is_valid_ = False
    return is_valid_

new_history['is_valid'] = new_history['message_parsed'].apply(lambda x: is_valid(x))
new_history = new_history[new_history['is_valid']==True]

if len(list(new_history.index)) > 0:
    for i in list(new_history.index):
        if len(new_history.message_parsed[i]) == 2:
            current_date = pd.to_datetime('today').strftime("%-m/%-d/%Y")
            category = new_history.message_parsed[i][0]
            spending = new_history.message_parsed[i][1]
        elif len(new_history.message_parsed[i]) == 3:
            current_date = pd.to_datetime(new_history.message_parsed[i][0]).strftime("%-m/%-d/%Y")
            category = new_history.message_parsed[i][1]
            spending = new_history.message_parsed[i][2]

        gc = gspread.service_account(filename='service_account.json')
        sh = gc.open_by_key("1WbDYJoOETGZ9UPAXudjVpXcFup7FZjGEx5YdrveqJgY")
        worksheet = sh.get_worksheet(0)


        def target_cell_coordinates(category):
            categories_to_edit = {'Food groceries': 30,
                                  'Food outside': 31,
                                  'Flat': 32,
                                  'PS5 Games': 33,
                                  'Accessories': 34,
                                  'Cinema': 35,
                                  'Clothes': 36,
                                  'Connectivity': 37,
                                  'Rails': 38,
                                  'Museums': 39,
                                  'Tech Toys': 40,
                                  'Other': 41}
            row_to_edit = categories_to_edit[category]
            column_to_edit = worksheet.row_values(5).index(current_date)

            return row_to_edit, column_to_edit


        row_to_edit, column_to_edit = target_cell_coordinates(category)

        # print(current_date, category, spending)
        # print(row_to_edit, column_to_edit)

        formula = worksheet.cell(row_to_edit, column_to_edit, value_render_option='FORMULA').value
        # print(formula)
        if formula is not None:
            formula += '+'+str(spending)
        else:
            formula = '='+str(spending)
        # print(formula)

        worksheet.update_cell(row_to_edit, column_to_edit, formula)


    client.send_message('w9ME0Iixm9mMDMy', '[bot] Everything accounted')

    old_history = pd.concat([old_history, new_history])
    old_history.reset_index(drop=True, inplace=True)
    old_history.to_csv('history.csv')
else:
#     with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
    client.send_message('w9ME0Iixm9mMDMy', '[bot] Nothing to add')

def send_daily_stats(worksheet=worksheet):
    message = '[bot] Daily Stats\n**Category: Actual | Avg. per day | FC Month**'
    for i in range(49,62):
        stata = worksheet.row_values(i)[17:21]
        message += '\n'+stata[0]+': '+stata[1]+' | '+stata[2]+' | '+stata[3]
    return message

client.send_message('w9ME0Iixm9mMDMy', send_daily_stats())