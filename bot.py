import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import subprocess
import re

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Function to handle the /start command
def start(update, context):
    update.message.reply_text('Welcome to VideoManipulationBot! Send me a video file and use commands like /addmetadata, /removemetadata, /removeaudio, /createqualities.')

# Function to handle the /addmetadata command
def add_metadata(update, context):
    update.message.reply_text('Adding metadata...')
    # Replace 'input.mkv' and 'output.mkv' with your desired file names
    subprocess.run(['ffmpeg', '-i', 'input.mkv', '-metadata', 'title="New Title"', 'output.mkv'])
    update.message.reply_text('Metadata added successfully!')

# Function to handle the /removemetadata command
def remove_metadata(update, context):
    update.message.reply_text('Removing metadata...')
    # Replace 'input.mkv' and 'output.mkv' with your desired file names
    subprocess.run(['ffmpeg', '-i', 'input.mkv', '-map_metadata', '-1', 'output.mkv'])
    update.message.reply_text('Metadata removed successfully!')

# Function to handle the /removeaudio command
def remove_audio(update, context):
    update.message.reply_text('Removing audio...')
    # Replace 'input.mkv' and 'output.mkv' with your desired file names
    subprocess.run(['ffmpeg', '-i', 'input.mkv', '-c', 'copy', '-an', 'output.mkv'])
    update.message.reply_text('Audio removed successfully!')

# Function to handle the /createqualities command
def create_qualities(update, context):
    update.message.reply_text('Creating multiple qualities...')
    # Replace 'input.mkv' and 'output.mkv' with your desired file names
    subprocess.run(['ffmpeg', '-i', 'input.mkv', '-c:v', 'libx264', '-preset', 'slow', '-b:v', '500k', '-s', '640x360', '-c:a', 'aac', '-b:a', '128k', 'output_low.mkv'])
    subprocess.run(['ffmpeg', '-i', 'input.mkv', '-c:v', 'libx264', '-preset', 'slow', '-b:v', '1000k', '-s', '1280x720', '-c:a', 'aac', '-b:a', '128k', 'output_medium.mkv'])
    subprocess.run(['ffmpeg', '-i', 'input.mkv', '-c:v', 'libx264', '-preset', 'slow', '-b:v', '2000k', '-s', '1920x1080', '-c:a', 'aac', '-b:a', '128k', 'output_high.mkv'])
    update.message.reply_text('Multiple qualities created successfully!')

# Function to handle videos sent by users
def handle_video(update, context):
    update.message.reply_text('Processing video...')
    # Download the video file
    video_file = context.bot.get_file(update.message.video.file_id)
    video_file.download('input.mkv')
    update.message.reply_text('Video downloaded successfully!')
    # Inform the user that processing has begun
    update.message.reply_text('Processing...')
    # Do something with the video (e.g., add metadata, remove audio, etc.)
    # After processing, send the processed video back to the user
    context.bot.send_chat_action(update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)
    with open('output.mkv', 'rb') as video:
        update.message.reply_video(video)
    update.message.reply_text('Video processed and sent!')

# Function to handle FFmpeg progress
def ffmpeg_progress(process):
    while True:
        line = process.stderr.readline()
        if not line:
            break
        line = line.decode("utf-8")
        if "frame=" in line:
            frame = re.search(r"frame=\s*([0-9]+)", line).group(1)
            total = re.search(r"fps=\s*[0-9]+.*total_size=\s*([0-9]+)", line).group(1)
            percent = (int(frame) / int(total)) * 100
            print(f"Processing... {percent:.2f}%")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addmetadata", add_metadata))
    dp.add_handler(CommandHandler("removemetadata", remove_metadata))
    dp.add_handler(CommandHandler("removeaudio", remove_audio))
    dp.add_handler(CommandHandler("createqualities", create_qualities))
    dp.add_handler(MessageHandler(Filters.video, handle_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
