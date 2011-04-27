import os
import re
import sys
import time
import logger
import mail
from threading import Thread
from PyGtalkRobot import GtalkRobot

#########################################################################################

class sendRecMessage(Thread):
   def __init__ (self, bot, count, user, sleepTime, message):
      Thread.__init__(self)
      self.sleepTime = sleepTime
      self.message = message
      self.user = user
      self.bot = bot
      self.count = count

   def run(self):
      i = 0
      while i < int(self.count):
      	time.sleep(float(self.sleepTime))
	bot.send(self.user, self.message)
	i = i + 1

class sendMessage(Thread):
   def __init__ (self, bot, user, sleepTime, message):
      Thread.__init__(self)
      self.sleepTime = sleepTime
      self.message = message
      self.user = user
      self.bot = bot

   def run(self):
      time.sleep(float(self.sleepTime))
      bot.send(self.user, self.message)


class SampleBot(GtalkRobot):
    
    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets
    
    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    #This method is used to change the state and status text of the bot.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == 'asheeshvarshneya@gmail.com':
            print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
            self.setState(show, status)
	    self.replyMessage(user, "State settings changed")

    def send(self, user, message):
	logger.WriteLogEvent("./sent.txt", str(user) + ":" + message)
	self.replyMessage(user, message)	

    def timediff(self, t):
	m =  time.strftime("%M", time.localtime())
	h = time.strftime("%H", time.localtime())

	mm=0
	hh=0
	flag = 0

	mm = int(t.split(':')[1])-int(m)
	if mm < 0:
		mm = mm + 60
		flag = 1
	
	hh = int(t.split(':')[0])-int(h)
	if flag == 1:
		hh = hh - 1
	if hh < 0:
		hh = hh + 24

	sec = (hh*60+mm)*60
	return sec		

    #This method is used to send email for users.
    def command_002_SendEmail(self, user, message, args):
        #email ldmiao@gmail.com hello dmeiao, nice to meet you, bla bla ...
        '''(?:email|mail|em|m)\s+(.*?@.+?)\s+(.*?),\s*(.*?)(?i)'''
        email_addr = args[0]
        subject = args[1]
        body = args[2]
	print message
        #call_send_email_function(email_addr, subject,  body)
        
        self.replyMessage(user, "\nEmail sent to "+ email_addr +" at: "+time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
    
    def command_002_sendLogs(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(logs)'''
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == 'asheeshvarshneya@gmail.com':
	    mail.sendMail("asheeshvarshneya@gmail.com","logs of remindme","Logs are attached","sent.txt")
	    mail.sendMail("asheeshvarshneya@gmail.com","logs of remindme","Logs are attached","logs.txt")
	    self.replyMessage(user, "mail sent")

    def command_002_faltu(self, user, message, args):
	'''(Invalid input. Type 'help' to know the options.)(?i)'''
	return ''

    def command_019_reminder1(self, user, message, args):
	'''(remind)( *[0-9]+)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendMessage(self, user, float(args[1])*60, args[2])
	m.start()

    def command_011_reminder2(self, user, message, args):
	'''(remind)( *[0-9]*)(?:m|min)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendMessage(self, user, float(args[1])*60, args[3])
	m.start()
    def command_012_reminder3(self, user, message, args):
	'''(remind)( *[0-9]*)(?:s|sec)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendMessage(self, user, float(args[1]), args[3])
	m.start()
    def command_013_reminder4(self, user, message, args):
	'''(remind)( *[0-9]*)(?:h|hour)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendMessage(self, user, float(args[1])*60*60, args[3])
	m.start()

    def command_014_reminder5(self, user, message, args):
	'''(remind)( *[0-9][0-9]?:[0-9][0-9]?)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendMessage(self, user, float(self.timediff(args[1])), args[2])
	m.start()


    def command_029_reminder6(self, user, message, args):
	'''(remind rec)( *[0-9]*)( *[0-9]+)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendRecMessage(self, args[1], user, float(args[2])*60, args[3])
	m.start()

    def command_021_reminder7(self, user, message, args):
	'''(remind rec)( *[0-9]*)( *[0-9]*)(?:m|min)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendRecMessage(self, args[1], user, float(args[2])*60, args[4])
	m.start()
    def command_022_reminder8(self, user, message, args):
	'''(remind rec)( *[0-9]*)( *[0-9]*)(?:s|sec)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendRecMessage(self, args[1], user, float(args[2]), args[4])
	m.start()
    def command_023_reminder9(self, user, message, args):
	'''(remind rec)( *[0-9]*)( *[0-9]*)(?:h|hour)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendRecMessage(self, args[1], user, float(args[2])*60*60, args[4])
	m.start()

    def command_024_reminder10(self, user, message, args):
	'''(remind rec)( *[0-9]*)( *[0-9][0-9]?:[0-9][0-9]?)( +(.*))?$(?i)'''
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
	m = sendRecMessage(self, args[1], user, float(self.timediff(args[2])), args[3])
	m.start()

    def command_009_testing(self, user, message, args):
	'''(asheesh rec)( *[0-9]*)( *[0-9]*)(?:h|hour)( +(.*))?$(?i)'''
	#m = sendMessage(self, user, args[1].split(" ")[1], ' '.join(args[1].split(" ")[2:]))
	#m.start()
	self.send(user, "Message Scheduled!!. Thanks for using 'remindme'.")
	self.send(user, args[2])
	#self.replyMessage(user, ' '.join(args[1].split(" ")[2:]))

    def command_009_hi(self, user, message, args):
        '''(hi|hello|hey)(?i)'''
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
        self.replyMessage(user, "Hi... Thanks for using 'remindme'. Type 'help' to know the options.")

    def command_004_time(self, user, message, args):
	'''(time)(?i)'''
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
        self.replyMessage(user, time.strftime("%H:%M:%S %a %d-%m-%Y", time.localtime()))

    def command_005_info(self, user, message, args):
	'''(info)(?i)'''
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
        self.replyMessage(user, 'For detailed info visit: http://www.asheesh.in/remindme')
    def command_006_support(self, user, message, args):
	'''(support)(?i)'''
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
        self.replyMessage(user, 'Contact us at: asheeshvarshneya@gmail.com' )
    def command_007_contact(self, user, message, args):
	'''(contact)(?i)'''
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
        self.replyMessage(user, 'Contact us at: asheeshvarshneya@gmail.com')
    def command_003_help(self, user, message, args):
	'''(help)(?i)'''
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
        self.replyMessage(user, "\n------------*Help*------------\nPossible options:\n\tremind <time><sec|min|hour> <message>\n\tremind rec <count> <time><sec|min|hour> <message>\nOr type:\n'info' - remindme basics.\n'support' - get assistance.\n'contact' - give feedback or suggesstion or just wanna write to us")

    #This method is used to response users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
	logger.WriteLogEvent("./logs.txt", str(user) + ":" + message)
        self.replyMessage(user, "Invalid input. Type 'help' to know the options.")

#########################################################################################
if __name__ == "__main__":
    bot = SampleBot()
    bot.setState('available', "Asheesh's ReminderBot Beta")
    bot.start("foo@gmail.com", "password")
