import os
import requests
import json

## Function to sendMessage to Telegram
def SendMarkdown(chat_id='509161525', text='*Hey this is Markdown*', token=os.environ.get("TELEGRAM_API_TOKEN"), parse_mode="MarkdownV2"):  ## Specify chat_id and text message
    
    BASE_URI = "https://api.telegram.org"

    full_token = f"bot{token}"
    action = "sendMessage"

    url = f"{BASE_URI}/{full_token}/{action}"

    params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode
    }

    req = requests.get(url=url, params=params)
    return req.json()


if __name__ == '__main__':
    ## Get Telegram API Token
    token = os.environ.get('TELEGRAM_API_TOKEN')
    text = "*Hey*, This is ```Markdown``` _Yeah_"
    print(SendMarkdown(text=text, token=token))