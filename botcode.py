import telebot
import os

# Set your Bot Token here
BOT_TOKEN = "Telegram Bot Token"

# Creating Telebot Object
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store subject progress
subject_progress = {}

# Define subjects and chapters
subjects = {
    "P1P": ["2", "4", "5", "6", "7", "8", "10"],
    "P2P": ["1", "2", "3", "7", "8", "9", "10"],
    "C1P": ["2", "3", "4", "5"],
    "C2P": ["1", "2", "3", "4"],
    "B1P": ["1", "2", "4", "7", "8", "9", "11"],
    "B2P": ["1", "2", "3", "4", "5", "7", "11"],
    "M1P": ["1", "3", "4", "7", "9", "10"],
    "M2P": ["3", "4", "6", "7", "8", "9"]
}

# Whenever Starting Bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    reply_text = "Welcome to the Subject Progress Bot!\n\n" \
                 "Please enter the subject name and the number of chapters completed.\n" \
                 "Use the format: /progress subject_name chapters_completed"

    bot.reply_to(message, reply_text)

# Track subject progress
@bot.message_handler(commands=['progress'])
def track_progress(message):
    args = message.text.split()[1:]
    if len(args) != 2:
        reply_text = "Invalid format! Please use the format: /progress subject_name chapters_completed"
    else:
        subject_name = args[0]
        chapters_completed = args[1].split(",")
        if subject_name in subjects:
            subject_progress[subject_name] = chapters_completed
            reply_text = f"Progress for {subject_name} updated. Chapters completed: {', '.join(chapters_completed)}"
        else:
            reply_text = f"Invalid subject! Please enter a valid subject."

    bot.reply_to(message, reply_text)

# Show subject progress
@bot.message_handler(commands=['showprogress'])
def show_progress(message):
    if not subject_progress:
        reply_text = "No progress tracked yet."
    else:
        reply_text = "Subject Progress:\n"
        for subject, chapters_completed in subject_progress.items():
            completion_icons = ["✅" if ch in chapters_completed else "❌" for ch in subjects[subject]]
            remaining_chapters = [ch for ch in subjects[subject] if ch not in chapters_completed]
            progress = (len(chapters_completed) / len(subjects[subject])) * 100
            reply_text += f"{subject}: {' '.join(completion_icons)} {progress}% completed\n"
            if remaining_chapters:
                reply_text += f"Remaining chapters: {', '.join(remaining_chapters)}\n"
            reply_text += "\n"

    bot.reply_to(message, reply_text)

# Save subject progress as a text file and send as a document
@bot.message_handler(commands=['senddocument'])
def send_document(message):
    if not subject_progress:
        reply_text = "No progress tracked yet."
    else:
        # Create a text file with subject progress
        file_name = "subject_progress.txt"
        with open(file_name, "w") as file:
            file.write("Subject Progress:\n")
            for subject, chapters_completed in subject_progress.items():
                completion_icons = ["✅" if ch in chapters_completed else "❌" for ch in subjects[subject]]
                remaining_chapters = [ch for ch in subjects[subject] if ch not in chapters_completed]
                progress = (len(chapters_completed) / len(subjects[subject])) * 100
                file.write(f"{subject}: {' '.join(completion_icons)} {progress}% completed\n")
                if remaining_chapters:
                    file.write(f"Remaining chapters: {', '.join(remaining_chapters)}\n")
                file.write("\n")

        # Send the text file as a document
        with open(file_name, "rb") as file:
            bot.send_document(message.chat.id, file)

        # Delete the text file
        os.remove(file_name)

        reply_text = "Subject progress sent as a document."

    bot.reply_to(message, reply_text)

    bot.reply_to(message, reply_text, parse_mode='Markdown')

print("Bot started and waiting for new messages\n")

# Waiting for new messages
bot.polling()
