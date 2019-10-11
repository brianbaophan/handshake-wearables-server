from bluepy import btle
import time
import binascii
import smtplib
import boto3

import config

client = boto3.resource('dynamodb')
info_table= client.Table('User-Information')
id_table=client.Table('User-ID')


id_tags = {'C6FE7640':1, '26FF7640':2, '36187440':3, '96187440':4, 'F6187440':5, '76277540':6 , 'D6277540': 7, '660B7640': 8}


def get_user_info(user_id):
        info = dict()
        response = info_table.get_item(
        Key={'User': user_id})
        info['Email'] = response['Item']['Email']
        info['URL'] = response['Item']['URL']
        info['Occupation'] = response['Item']['Occupation']
        info['Company'] = response['Item']['Company']
        info['First_Name'] = response['Item']['First_Name']
        info['Last_Name'] = response['Item']['Last_Name']
        return info


def get_user_id(id):
        response = id_table.get_item(
        Key={'Tag': id})
        return response['Item']['User']
  

def create_message(this_user, info_dict):
        message = 'Hey ' + this_user + ',\n'
        message += '\n'
        message += 'You made a new connection with ' + info_dict['First_Name'] + ' ' + info_dict['Last_Name'] + '! You can see your new connection\'s details below:\n'
        message += '\n'
        message += 'Occupation: ' + info_dict['Occupation'] + '\n' 
        message += 'Company: ' + info_dict['Company'] + '\n' 
        message += '\n' 
        message += 'You may reach out to ' + info_dict['First_Name'] + ' at ' + info_dict['Email'] + '\n' 
        message += '\n'
        message += 'Additional information may be found at ' + info_dict['URL'] + '\n' 
        message += '\n' 
        message += 'Thank you for using the Shake. Handshake boy out!'
        return message


def send_email(subject, msg, email):
        try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(config.EMAIL_ADDRESS, config.PASSWORD)
                message = 'Subject: {}\n\n{}'.format(subject, msg)
                server.sendmail(config.EMAIL_ADDRESS,email, message)
                server.quit()
                print ('Success: Email sent!')
        except:
                print('Email failed to send.')


def get_data(dev):
        time.sleep(4)
        print 'Looking for user tags...'
        LairdMessage = btle.UUID('a6d81c26-3f48-48be-9eb8-b4a60c7dbe14')
        service = dev.getServiceByUUID(LairdMessage)
        LairdValue = btle.UUID('0001')
        value = service.getCharacteristics(LairdValue)[0]
        val = value.read()
        print 'User tags: ' + val
        try:
                time.sleep(4)
                dev.disconnect()
                print '1st attempt | Sucessfully disconnected with peripheral'
        except:
                print 'Unable to disconnect with peripheral'
        return val


def server(val):
        splitVal = val.split()

        this_user = get_user_id(id_tags[splitVal[0]])
        other_user = get_user_id(id_tags[splitVal[1]])

        this_user_info = dict()
        other_user_info = dict()

        this_user_info = get_user_info(this_user)
        other_user_info = get_user_info(other_user)

        message = create_message(this_user_info['First_Name'], other_user_info)
        send_email('You have a new connection!', message, this_user_info['Email'])


while True:
        try:
                time.sleep(3)
                print 'Connecting with f2:a4:c6:d9:5c:29...'
                dev = btle.Peripheral('f2:a4:c6:d9:5c:29', btle.ADDR_TYPE_RANDOM)
                print 'Connection is established'
                val = get_data(dev)
                try:
                        time.sleep(3)
                        dev.disconnect()
                        print '2nd attempt | Sucessfully disconnected with peripheral'
                except:
                        print 'No connections with peripheral'
                server(val)
        except:
                print 'Unable to connect with f2:a4:c6:d9:5c:29'
        try:
               time.sleep(3)
               print 'Connecting with ed:a4:0f:71:1d:f5...'
               dev = btle.Peripheral('ed:a4:0f:71:1d:f5', btle.ADDR_TYPE_RANDOM)
               print 'Connection is established'
               val = get_data(dev)
              try:
                       time.sleep(3)
                       dev.disconnect()
                       print '2nd attempt | Sucessfully disconnected with peripheral'
               except:
                       print 'No connections with peripheral'
              server(val)
        except:
               print 'Unable to connect with ed:a4:0f:71:1d:f5'
        try:
                time.sleep(3)
                print 'Connecting with f4:16:f7:48:8c:03...'
                dev = btle.Peripheral('f4:16:f7:48:8c:03', btle.ADDR_TYPE_RANDOM)
                print 'Connection is established'
                val = get_data(dev)
                try:
                        time.sleep(3)
                        dev.disconnect()
                        print '2nd attempt | Sucessfully disconnected with peripheral'
                except:
                        print 'No connections with peripheral'
                server(val)
        except:
                print 'Unable to connect with f4:16:f7:48:8c:03'
        continue
