import instaloader
import re
import os
import time
import requests
from telegram import Update,InputMediaPhoto,InputMediaVideo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
# ig = instaloader.Instaloader()

bot_token = '7336498837:AAFePhCo1RjFegTWwi3gQ5emjOt9qbCmS70'
chat_id = '-1002076457708'

sessionid ='53337164038%3AM21mEsh0cRYZ5N%3A2%3AAYeYaoXumNPgaGeaA1_zAPOS8zn2WyOP8yvTi6Q4Vg'
# Instaloader settings
logging.basicConfig(level=logging.INFO)
ig = instaloader.Instaloader()
# L.login('vinay_kr_official', 'Vinaykr@75')
ig.context.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
ig.context.max_connection_attempts = 1
ig.context._session.cookies.update({
    'sessionid': sessionid,
    'csrftoken': '9u7LQv35q7JwHJHYoZw0A8DfQiu7TjGB',  # Replace with your actual csrftoken
    'ds_user_id': '53337164038'    # Replace with your actual user ID
})

pathname = 'instafiles'

def insta(url):
   ig.dirname_pattern = pathname + '/{target}'
   try:
     profile = instaloader.Post.from_shortcode(ig.context,url.split("/")[-2])
     ig.download_post(profile,target=profile.url.split("/")[-2])
     time.sleep(2)
   except Exception as e:
     print(e)


async def start_cmd(update:Update,context: ContextTypes):
    await update.message.reply_text('''Hi! This bot helps you to save photos, videos, carousels and many more from Instagram.
To get photo/video/carousel/reels/IGTV send URL of the post to the bot.''')

async def img(update:Update,context: ContextTypes):
    await update.message.reply_chat_action(action='typing')
    current_directory = pathname
    directories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
    first_directory = os.path.join(current_directory, sorted(directories)[0])
    images = [f for f in os.listdir(first_directory) if os.path.isfile(os.path.join(first_directory, f)) and f.lower().endswith(('png', 'jpg', 'jpeg','txt','json.xz','gif','mp4',))]
    image_url = []
    if images:
        for image in images:
            image_path = os.path.join(first_directory, image)
            if image_path.endswith(('jpg','jpeg','png','gif')):
               try:
                  image_url.append(InputMediaPhoto(open(image_path, 'rb')))
               except Exception as e:
                   print(f'{e}')  
            os.remove(image_path)
            dir = os.listdir(first_directory)
            if len(dir)==0:
               os.rmdir(first_directory) 
        print(image_url)
        await update.message.reply_media_group(media=image_url,reply_to_message_id=update.message.message_id)       
        message = f'<b>If you want to get latest tech knowledge then you should have to vist our tech youtube channel <a href="https://www.youtube.com/@imagentech5414">Image N Tech</a> and do not forget to subscribe your channel.</b>'
        await update.message.reply_html(message)         
    else:
       await update.message.reply_text("No images found in the folder.")

async def reel(update:Update,context: ContextTypes):
    await update.message.reply_chat_action(action='typing')
    current_directory = pathname
    directories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
    first_directory = os.path.join(current_directory, sorted(directories)[0])
    images = [f for f in os.listdir(first_directory) if os.path.isfile(os.path.join(first_directory, f)) and f.lower().endswith(('png', 'jpg', 'jpeg','txt','json.xz','gif','mp4',))]
    image_url = []
    if images:
        for image in images:
            image_path = os.path.join(first_directory, image)
            if image_path.endswith(('mp4')):
               try:
                   image_url.append(InputMediaVideo(open(image_path, 'rb')))
               except Exception as e:
                   print(f'{e}')  
            os.remove(image_path)
            dir = os.listdir(first_directory)
            if len(dir)==0:
               os.rmdir(first_directory) 
        await update.message.reply_media_group(media=image_url,reply_to_message_id=update.message.message_id)       
        message = f'<b>If you want to get latest tech knowledge then you should have to vist our tech youtube channel <a href="https://www.youtube.com/@imagentech5414">Image N Tech</a> and do not forget to subscribe your channel.</b>'
        await update.message.reply_html(message)        
    else:
       await update.message.reply_text("No images found in the folder.")      

async def img_cmd(update:Update,context: ContextTypes):
    await update.message.reply_text('Please past the URL')

async def vid_cmd(update:Update,context: ContextTypes):
    await update.message.reply_text('Please past the URL')



def handle_response(text: str) -> str:
    processed : str = text.lower()
    if 'hello' in processed:
        return 'Hey there'

    if 'good morning' in processed:
        return 'Hey there good morning'

    if processed.startswith('https://www.instagram.com/reel'):
       insta(text)
       return 'Click here /generate_reel'

    if processed.startswith('https://www.instagram.com/'):
       insta(text)
       return 'Click here /generate'

    return 'Sorry i am not able to understand'

async def handel_message(update:Update,context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}')

    if text.startswith('https://www.instagram.com/'):   
      await update.message.reply_text('Please wait while we make the file....')
      await update.message.reply_chat_action(action='typing')
    response: str = handle_response(text)
    print('Bot:',response)
    await update.message.reply_text(response)


if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(bot_token).build()

    app.add_handler(CommandHandler('start',start_cmd))
    app.add_handler(CommandHandler('image',img_cmd))
    app.add_handler(CommandHandler('video',vid_cmd))
    app.add_handler(CommandHandler('generate',img))
    app.add_handler(CommandHandler('generate_reel',reel))

    app.add_handler(MessageHandler(filters.TEXT,handel_message))

    app.run_polling(poll_interval=3)
