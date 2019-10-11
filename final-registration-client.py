from oauth2client.service_account import ServiceAccountCredentials
import gspread 
import boto3
import time

client = boto3.resource('dynamodb')
info_table= client.Table('User-Information')
id_table=client.Table('User-ID')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Event Registration (Responses)').sheet1


id_tags = ['C6FE7640', '26FF7640', '36187440', '96187440', 'F6187440', '76277540', 'D6277540', '660B7640']
length = 3


def store_id(record):

    user = record['First Name'][0].lower() + record['Last Name'].lower()

    id_table.put_item(Item={'ID': id_tags[record['ID Tag'] - 1],
                            'Tag': record['ID Tag'],
                            'User': user})
    
    print 'Successfully stored user ID for ' + user 

    return user


def store_info(record, user):

    info_table.put_item(Item={'User': user,
                              'Company': record['Company'],
                              'Email': record['Email'],
                              'First_Name': record['First Name'],
                              'Last_Name': record['Last Name'],
                              'Occupation': record['Occupation'],
                              'URL': record['LinkedIn URL']})

    print 'Successfully stored user information for ' + user


while True:
    time.sleep(5)

    print 'Checking for new users...'

    records = sheet.get_all_records()

    if len(records) > length:
        new_user_count = str(len(records) - length)
        if new_user_count is 1:
            print 'Found ' + new_user_count + ' new user'
        elif new_user_count > 1:
            print 'Found ' + new_user_count + ' new users'

        print 'Entering new users into database...'

        for i in range(length, len(records)):
            if records[i]['LinkedIn URL'] is '':
                records[i]['LinkedIn URL'] = 'N/A'
            user = store_id(records[i])
            store_info(records[i], user)

        length = len(records)
    
    else:
        print 'Unable to find new users'
