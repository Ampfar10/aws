import boto3
import time
import requests
from datetime import datetime
from telegram.ext import Updater, CommandHandler

# Replace with the ID of the instance you want to check
instance_id = 'i-0cf02d530e32dbd07'

# Replace with your Telegram bot token and chat ID
telegram_token = '5433855776:AAH5RAL6rrKla3hxygyYhjAwSjVmudbDNUw'
telegram_chat_id = '2123403786'

# specify the region
session = boto3.Session(region_name='af-south-1')
ec2 = session.client('ec2')

def start(update, context):
    #get the instance status
    instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    instance_status = instance['State']['Name']
    instance_ip = instance.get('PublicIpAddress', "Not Assigned")
    message = f"Instance ID: {instance_id}\nInstance Status: {instance_status}\nPublic IP: {instance_ip}"
    update.message.reply_text(message)


updater = Updater(telegram_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()

def check_instance_status():
    try:
        # Describe the instance and check its status
        response = ec2.describe_instance_status(InstanceIds=[instance_id])
        status = response['InstanceStatuses'][0]['InstanceStatus']['Status']
        system_status = response['InstanceStatuses'][0]['SystemStatus']['Status']

        # Check if the status check has failed
        if status == "impaired" and system_status == "impaired":
            send_message_telegram(f'[{datetime.now()}] Instance {instance_id} has failed status check')
            return False
        else:
            send_message_telegram(f'[{datetime.now()}] Instance {instance_id} is healthy')
            return True
    except Exception as e:
        send_message_telegram(f'[{datetime.now()}] An error occurred: {e}')
        return False

def shutdown_instance():
    try:
        # Shut down the instance
        ec2.stop_instances(InstanceIds=[instance_id])
        send_message_telegram(f'[{datetime.now()}] Instance {instance_id} has been shut down')
    except Exception as e:
        send_message_telegram(f'[{datetime.now()}] An error occurred: {e}')

def start_instance():
    try:
        # Start the instance
        ec2.start_instances(InstanceIds=[instance_id])
        send_message_telegram(f'[{datetime.now()}] Instance {instance_id} is starting')
    except Exception as e:
        send_message_telegram(f'[{datetime.now()}] An error occurred: {e}')

def get_instance_ip():
    try:
        # Get the public IP of the instance
        response = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        send_message_telegram(f'[{datetime.now()}] Public IP of instance {instance_id} is {public_ip}')
        return public_ip
    except Exception as e:
        send_message_telegram(f'[{datetime.now()}] An error occurred: {e}')
        return None

def send_message_telegram(message):
    try:
        # Send message to Telegram
        url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        data = {'chat_id': telegram_chat_id, 'text': message}
        requests.post(url, data)
    except Exception as e:
        send_message_telegram(f'[{datetime.now()}] An error occurred: {e}')

if not check_instance_status():
    shutdown_instance()
    time.sleep(600)
    start_instance()
    time.sleep(60) # wait for 1 minute for the instance to fully start
    ip = get_instance_ip()
    if ip:
        send_message_telegram(f'[{datetime.now()}] Instance {instance_id} has been successfully restarted. Public IP: {ip}')
    else:
        send_message_telegram(f'[{datetime.now()}] Instance {instance_id} has been successfully restarted but could not fetch the IP')
