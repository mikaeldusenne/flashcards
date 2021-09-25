import boto3
from botocore.exceptions import ClientError
from typing import List, Set, Dict, Tuple, Optional, Union, NewType, Any
import logging
from os import environ

from backend.src import helpers as h
from backend.src import db

from markdown import markdown

CHARSET = "UTF-8"
mail_address = environ['MAIL_SENDER_ADDRESS']

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
# CONFIGURATION_SET = "ConfigSet"

client = boto3.client('ses', region_name="us-east-1")


def sendf(recipients: List[str], subject: str, body_text: str, body_html: str) -> Union[None, str]:
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': recipients,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=mail_address
        )
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        return None
    else:
        logging.info(f"@@@@email@@@@ Email sent to {recipients}! Message ID: {response['MessageId']}")
        return response['MessageId']


def send_email(recipients, subject, body_text):
    if type(recipients) == str:
        recipients = recipients.split(',')
    sendf(recipients, subject, body_text=body_text, body_html=markdown(body_text))


def send_email_with_link(recipients, link, reason="confirm your email"):
    send_email(
        recipients,
        "Mikarezoo Flashcards - Confirm your email",
        f"""### Welcome to Mikarezoo Flashcards

To {reason}, please click on [this link]({link}).

If the link above doesn't work, please copy and paste the following url to your web browser:  
{link}

See you soon on Mikarezoo Flashcards!
"""
    )

if __name__=="__main__":
    from sys import argv
    send_email(
        argv[1],
        "test ses",
        "# Test SES\n--------\nHello, this is a *ses* test\n----"
    )
