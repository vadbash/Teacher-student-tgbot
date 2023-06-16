#import all libraries
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
import re
import mysql.connector

db_name = "db_name"
db_username = "db_username"
db_password = "db_password"

#connection to MySQL
connection = mysql.connector.connect(host="localhost",
                                    database=db_name,
                                    user=db_username,
                                    password=db_password,
                                    auth_plugin='mysql_native_password')

cursor=connection.cursor()
table = "table_name"

#apply bot token
bot = telebot.TeleBot('Your_token')

#start function
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton("Educator 👨‍🏫")
    btn2 = types.InlineKeyboardButton("Students 👨‍🎓👩‍🎓")
    markup.add(btn1, btn2) #if you have an account chose Login 🔐, if not - Registration ®️
    bot.reply_to(message, "Welcome, choose are you teacher 👨‍🏫 or student 👨‍🎓👩‍🎓", reply_markup=markup)

#function for students(login/registration)
@bot.message_handler(regexp='Students 👨‍🎓👩‍🎓')
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton("Registration ®️")
    btn2 = types.InlineKeyboardButton("Login 🔐")
    markup.add(btn1, btn2)
    bot.reply_to(message, "Hello, if you have an account chose Login 🔐, if not - Registration ®️", reply_markup=markup)  

#registration for students
@bot.message_handler(regexp='Registration ®️')
def send_welcome(message):
    msg = bot.send_message(message.chat.id, text="Hello, enter your username: ")
    bot.register_next_step_handler(msg, reg)

def reg(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.InlineKeyboardButton("Choose teacher 👨‍🏫")
    markup.add(btn2)

    #connection to MySQL
    connection = mysql.connector.connect(host="localhost",
                                    database=db_name,
                                    user=db_username,
                                    password=db_password,
                                    auth_plugin='mysql_native_password')

    cursor=connection.cursor()

    name = message.text

    #defolt teahcer parametr
    teacher = "no"
    
    enter = cursor.execute(f"select name, teacher from {table} where name = %s and teacher = %s" ,(name, teacher))

    if name == '':
        bot.send_message(message.chat.id, text="Username is empty")
        exit()


    if cursor.fetchone() is None:

        cursor.execute(f"insert into {table}(name, teacher) values(%s, %s)" ,(name, teacher))
        connection.commit()
        bot.send_message(message.chat.id, text="Regestration successful", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="User with such name is already registered, try one more time later")

    cursor.execute(f"select * from {table}")
    data=cursor.fetchall()
    cursor.close()

#login function for students
@bot.message_handler(regexp='Login 🔐')
def send_welcome(message):
    msg = bot.send_message(message.chat.id, text="Hello, enter your username: ")
    bot.register_next_step_handler(msg, login)
    
def login(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton("List 🔔")
    btn2 = types.InlineKeyboardButton("Send work ✒️")
    btn3 = types.InlineKeyboardButton("Communication 📱")
    btn4 = types.InlineKeyboardButton("E-journal 📒")
    markup.add(btn1, btn2, btn3, btn4)

    #connection to MySQL
    connection = mysql.connector.connect(host="localhost",
                                    database=db_name,
                                    user=db_username,
                                    password=db_password,
                                    auth_plugin='mysql_native_password')

    cursor=connection.cursor()

    name = message.text
    #defolt teacher parametr
    teacher = "no"

    query = f"SELECT name, teacher FROM {table} WHERE name = %s"
    cursor.execute(query, (name,))

    if name == '':
        bot.send_message(message.chat.id, text="Your name is empty, try one more time later")
        exit()

    if not cursor.fetchone():
        bot.send_message(message.chat.id, text="You don't have an account")
    else:
        bot.send_message(message.chat.id, text="Login successful, HI", reply_markup=markup)

    cursor.execute(f"select * from {table}")
    data=cursor.fetchall()
    cursor.close()

#logining as teacher    
@bot.message_handler(regexp='Educator 👨‍🏫')
def welcome_teach(message):
    msg = bot.send_message(message.chat.id, text="Hello, enter your name: ")
    bot.register_next_step_handler(msg, login_teach)

def login_teach(message):
    with open('teachers.txt', 'r') as file:
        lines = file.readlines()
        name_to_find = message.text.title()
        found = False
        for line in lines:
            line = line.rstrip('\n')  # Remove the newline character
            if name_to_find in line:
                found = True
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.InlineKeyboardButton("List 🔔")
                btn2 = types.InlineKeyboardButton("Add tasks 📃")
                btn3 = types.InlineKeyboardButton("Send materials 🗣️🖋️")
                btn4 = types.InlineKeyboardButton("Communication 🗨️📱")
                btn5 = types.InlineKeyboardButton("E-journal 📒")
                markup.add(btn1, btn2, btn3, btn4, btn5)
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, text="Login successful, HI", reply_markup=markup)
        if not found:
            bot.send_message(message.chat.id, text="Such teacher wasn't found, try one more time")
            welcome_teach(message)  

#list with all students/disciplines/groups/teachers               
@bot.message_handler(regexp="List 🔔")
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    
    btn1 = InlineKeyboardButton('Students 👨‍🎓👩‍🎓', callback_data='button1')
    btn2 = InlineKeyboardButton('Disciplines 🏫', callback_data='button2')
    btn3 = InlineKeyboardButton('Groups 👥', callback_data='button3')
    btn4 = InlineKeyboardButton('List of teachers 👨‍🏫', callback_data='button4')
    
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text="Choose what you want to know:", reply_markup=keyboard)

#function for InlineKeyboardButton
@bot.callback_query_handler(func=lambda call: True)
def handle_button_response(call):
    connection = mysql.connector.connect(host="localhost",
                                    database=db_name,
                                    user=db_username,
                                    password=db_password,
                                    auth_plugin='mysql_native_password')

    cursor=connection.cursor()
    keyboard = InlineKeyboardMarkup()
    
    btn1 = InlineKeyboardButton('Students 👨‍🎓👩‍🎓', callback_data='button1')
    btn2 = InlineKeyboardButton('Disciplines 🏫', callback_data='button2')
    btn3 = InlineKeyboardButton('Groups 👥', callback_data='button3')
    btn4 = InlineKeyboardButton('List of teachers 👨‍🏫', callback_data='button4')
    
    keyboard.add(btn1, btn2, btn3, btn4)

    comm = InlineKeyboardMarkup()
    
    btn1 = InlineKeyboardButton('Communication 📱', callback_data='button5')
    comm.add(btn1)

    teach_comm = InlineKeyboardMarkup()
    
    btn1 = InlineKeyboardButton('Course 🗨️', callback_data='button6')
    btn2 = InlineKeyboardButton('Group 🗨️', callback_data='button7')
    
    teach_comm.add(btn1, btn2)
    #Students
    if call.data == 'button1':
        try:
            cursor.execute(f"select * from {table}")
            data=cursor.fetchall()
            all_user_data = []
            output = ""
            for row in data:
                a = row[1], row[2]
                all_user_data.append({a})
            for item in all_user_data:
                for key, value in item:
                    output += "👤 " + key + " " + value + "\n\n"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"*List of Students 👨‍🎓👩‍🎓* \n\n{output}",parse_mode='MarkdownV2', reply_markup=keyboard)
        except Exception:
            ...
    #Disciplines
    elif call.data == 'button2':
        try:
            with open('disciplines.txt', 'r') as file:
                text = file.read()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"*List of Disciplines 🏫* \n\n{text}", parse_mode='MarkdownV2', reply_markup=keyboard)
        except Exception:
            ...
    #Groups
    elif call.data == 'button3':
        try:
            with open('groups.txt', 'r') as file:
                text = file.read()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"*List of Groups 👥* \n\n{text}", parse_mode='MarkdownV2', reply_markup=keyboard)
        except Exception:
            ...
    #List of teachers
    elif call.data == 'button4':
        try:
            with open('teachers.txt', 'r') as file:
                lines = file.readlines()

        # Create a list to store the modified lines
                modified_lines = []

                # Iterate over each line
                for line in lines:
                    # Split the line into words
                    words = line.split()
                    
                    # Create the modified line
                    if len(words) > 1:
                        modified_line = '👨‍🏫 ' + ' '.join(words[:-1])
                        modified_lines.append(modified_line)
                    elif len(words) == 1:
                        modified_lines.append(words[0])

        # Print all the modified lines in one statement
                list_of_teachers = '\n\n'.join(modified_lines)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"*List of Teachers 👨‍🏫* \n\n{list_of_teachers}", parse_mode='MarkdownV2', reply_markup=keyboard)
        except Exception:
            ...
    #Communication
    elif call.data == 'button5':
        try:
            with open('teachers.txt', 'r') as file:
                lines = file.readlines()

                # Create an empty list
                modified_lines = []

                for line in lines:
                    words = line.split()
                    
                    # Create the modified line
                    if len(words) > 1:
                        modified_line = '👨‍🏫 ' + ' '.join(words)
                        modified_lines.append(modified_line)
                    elif len(words) == 1:
                        modified_lines.append(words[0])

                list_of_teachers = '\n\n'.join(modified_lines)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"*List of Teachers 👨‍🏫 and theirs numbers for communication* \n\n{list_of_teachers}", parse_mode='MarkdownV2', reply_markup=comm)

        except Exception:
            ...
    #Course
    elif call.data == 'button6':
        try:
            google_disk = re.escape("https://drive.google.com/drive")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"*Communication 🗨️📱 with course:\n\n There is the link on course*\n🌐{google_disk}", parse_mode='MarkdownV2', reply_markup=teach_comm)

        except Exception:
            ...
    #Group
    elif call.data == 'button7':
        try:
            google_disk = re.escape("https://drive.google.com/drive")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"*Group communication 🗨️📱:\n\n There is the link on course*\n🌐{google_disk}", parse_mode='MarkdownV2', reply_markup=teach_comm)

        except Exception:
            ...
    bot.answer_callback_query(call.id)

#Function where students choose teachers
@bot.message_handler(regexp="Choose teacher 👨‍🏫")
def choose_teacher(message):
    try:
        with open('teachers.txt', 'r') as file:
            lines = file.readlines()

            # Create an empty list
            modified_lines = []

            for line in lines:
                words = line.split()
                
                # Create the modified line
                if len(words) > 1:
                    modified_line = '👨‍🏫 ' + ' '.join(words[:-1])
                    modified_lines.append(modified_line)
                elif len(words) == 1:
                    modified_lines.append(words[0])

            list_of_teachers = '\n\n'.join(modified_lines)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text=f"*List of Teachers 👨‍🏫* \n\n{list_of_teachers}", parse_mode='MarkdownV2')
            msg = bot.send_message(message.chat.id, text="There is a list of teachers, if you want to choose one write his name there:")
            bot.register_next_step_handler(msg, define)
    except Exception:
        ...
#Login function after choosing teacher and add techer to student
def define(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton("Login 🔐")
    markup.add(btn1)
    #connection to MySQL
    cnx = mysql.connector.connect(host="localhost",
                                    database=db_name,
                                    user=db_username,
                                    password=db_password,
                                    auth_plugin='mysql_native_password')

    #Create a cursor object to interact with the database
    cursor = cnx.cursor()
    
    #adding teacher to student
    with open('teachers.txt', 'r') as file:
        lines = file.readlines()
        name_to_find = message.text.title()
        google_disk = re.escape("https://drive.google.com/drive")
        for line in lines:
            if name_to_find in line:
                query = f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1"
                cursor.execute(query)
                line = line.rstrip('\n')
                words = line.split()
                result = cursor.fetchone()
                update_query = f"UPDATE {table} SET teacher = %s WHERE id = %s"
            
                new_teacher = ' '.join(words[:-1])
                user_id = result[0]
                cursor.execute(update_query, (new_teacher, user_id))
                cnx.commit()

                cursor.close()
                cnx.close()
                bot.send_message(message.chat.id, text=f"*Сongratulations, you have become a student for 👨‍🏫 {' '.join(words[:-1])}* \nThere is a link on google disk, find there your teacher and start working: \n\n🌐 {google_disk}", parse_mode='MarkdownV2', reply_markup=markup)
                break
        else:
            bot.send_message(message.chat.id, text=f"*There are no teacher with name {message.text} try one more time*", parse_mode='MarkdownV2')
            choose_teacher(message)

#Add task for students from teacher
@bot.message_handler(regexp='Add tasks 📃')
def add_tasks(message):
    google_disk = re.escape("https://drive.google.com/drive")
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text = f"*Want to add some task for your students?*\n\nThen visit google disk and start working:\n🌐 {google_disk}",  parse_mode='MarkdownV2')

#Send work from student to teacher
@bot.message_handler(regexp='Send work ✒️')
def add_tasks(message):
    google_disk = re.escape("https://drive.google.com/drive")
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text = f"*To send your finished work to the teacher, click the link and find your teacher*\n\nLink on google disk:\n🌐 {google_disk}",  parse_mode='MarkdownV2')

#Add materials(lectures/labs)
@bot.message_handler(regexp='Send materials 🗣️🖋️')
def add_tasks(message):
    google_disk = re.escape("https://drive.google.com/drive")
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text = f"*Want to add some lectures and laboratory for your students?*\n\nThen visit google disk and start working:\n🌐 {google_disk}",  parse_mode='MarkdownV2')

#Communication for students with teachers
@bot.message_handler(regexp="Communication 📱")
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    
    btn1 = InlineKeyboardButton('Communication 📱', callback_data='button5')
    
    keyboard.add(btn1)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text="*Choose what you want to communicate with* 📱:", reply_markup=keyboard, parse_mode='MarkdownV2')

#Communication for teacher with course/groups
@bot.message_handler(regexp="Communication 🗨️📱")
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    
    btn1 = InlineKeyboardButton('Course 🗨️', callback_data='button6')
    btn2 = InlineKeyboardButton('Group 🗨️', callback_data='button7')
    
    keyboard.add(btn1, btn2)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text="Choose what you want to communicate with:", reply_markup=keyboard)

#Link to e-journal
@bot.message_handler(regexp="E-journal 📒")
def send_welcome(message):
    google_disk = re.escape("https://drive.google.com/drive")
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text=f"*There is a link to ejournal 📒* \n\n*Link*:\n🌐{google_disk}", parse_mode='MarkdownV2')

#starting bot
bot.polling()
