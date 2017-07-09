import discord
import asyncio
import aiohttp
import traceback
import sys
import os
import re
import datetime
import time
from datetime import datetime,tzinfo,timedelta
from random import randint


class FakeMember():
    def __init__(self, name):
        self.name = name
 
class PlaceHolder():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)
        
        
def is_bot(m):
	return m.author == client.user

        
print ('Logging into Discord...\n')
EQTest = {}
SubDict = {}
guestEnabled = {}
EQPostDict = {}
# Put the channel ID you want the parties to be made in
QuestChannelID = ''
# Set your ID to use the restart and shutdown commands
ownerID = ''
MPATitle = {}
PTauthor = {}
PTID = {}
participantCount = {}
appended = False
client = discord.Client()
getTime = datetime.now()

@asyncio.coroutine
def generateList(message, targetID, inputstring):
    pCount = 1
    nCount = 1
    mpaCount = 1
    alreadyWroteList = False
    playerlist = '\n'
    for word in EQTest[targetID]: 
        if nCount == 1:
            mpaCount += 1
        if (type(word) is PlaceHolder):
            playerlist += ('**>**' + '\n')
        else:
            playerlist += ('**>**' + " " + word + '\n')
        pCount+=1
        nCount+=1
        if nCount == 5:
            playerlist += ('\n')
            nCount = 1
        em = discord.Embed(description='', colour=0xB3ECFF)
        em.add_field(name='Party Name', value=MPATitle[targetID], inline=True)
        em.add_field(name='Party Status', value='`' + str(participantCount[targetID]) + '/' + '4 `', inline=True)
        em.add_field(name='Participant List', value=playerlist, inline=False)
        em.add_field(name='Last Action', value=inputstring, inline=False)
    try:
        yield from client.edit_message(EQPostDict[targetID], '', embed=em)
    except:
        EQPostDict[targetID] = yield from client.send_message(message.channel, '', embed=em)

            
@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith('%'):
        if message.content.lower().startswith('%creatept'):
            userstr = message.content
            userstr = userstr.replace("%creatept", "")
            if not message.author.id in EQTest:
                if message.author.top_role.permissions.send_tts_messages == True and message.channel.id == QuestChannelID:
                    EQTest[message.author.id] = list()
                    targetID = message.author.id
                    participantCount[message.author.id] = 0
                    for index in range(4):
                        EQTest[message.author.id].append(PlaceHolder(""))
                    MPATitle[message.author.id] = userstr
                    PTauthor[message.author.id] = message.author.name
                    yield from client.delete_message(message)
                    if isinstance(EQTest[targetID][0], PlaceHolder):
                        EQTest[targetID].pop(0)
                        EQTest[targetID].insert(0, message.author.name)
                        participantCount[targetID] += 1
                        yield from generateList(message, targetID, '```dsconfig\nStarting party! Please use %join @{}#{} to sign up!```'.format(message.author.name, message.author.discriminator))
                    log = yield from client.logs_from(message.channel, limit=2, after=message)
                    for message in log:
                        if message.author.id == client.user.id:
                            PTID[targetID] = message.id
                            break

                else:
                    yield from client.send_message(message.channel, 'You either are not in the right channel or you lack permissions to start a party!')
            else:
                targetID = message.author.id
                yield from generateList(message, targetID, '```fix\nYou already have a party list being made!```')
                yield from client.delete_message(message)
               
        elif message.content.lower().startswith('%join'):
            userstr = ''
            classRole = ''
            targetID = ''
            title = ''
            index = 0
            personInMPA = False
            if message.author.top_role.permissions.send_tts_messages == True and message.channel.id == QuestChannelID:
                userstr = message.content
                userstr = userstr.replace("%join", "")
                userstr = userstr.replace(" ", "")
                if userstr == '':
                    yield from client.send_message(message.channel, 'Who are you trying to join?')
                    return
                elif userstr.startswith('<@'):
                    if len(message.mentions) > 1:
                        yield from client.send_message(message.channel, 'You can only join one party at a time!')
                        return
                    elif message.mentions[0] != None:
                        targetID = message.mentions[0].id
                yield from client.delete_message(message)
                if targetID not in EQTest:
                    yield from client.send_message(message.channel, 'Party does not exist here!')
                    return
                for index, item in enumerate(EQTest[targetID]):
                    if (type(EQTest[targetID][index]) is PlaceHolder):
                        pass
                    elif message.author.name in item:
                        personInMPA = True
                        break
                for word in EQTest[targetID]:
                    if isinstance(word, PlaceHolder):
                        if personInMPA == False:
                            if isinstance(EQTest[targetID][0], PlaceHolder):
                                EQTest[targetID].pop(0)
                                EQTest[targetID].insert(0, classRole + ' ' + message.author.name)
                                participantCount[targetID] += 1
                                yield from generateList(message, targetID, '```diff\n+ {} has joined.```'.format(message.author.name))
                                appended = True
                                break
                            elif isinstance(EQTest[targetID][1], PlaceHolder):
                                EQTest[targetID].pop(1)
                                EQTest[targetID].insert(1, classRole + ' ' + message.author.name)
                                participantCount[targetID] += 1
                                yield from generateList(message, targetID,  '```diff\n+ {} has joined.```'.format(message.author.name))
                                appended = True
                                break
                            elif isinstance(EQTest[targetID][2], PlaceHolder):
                                EQTest[targetID].pop(2)
                                EQTest[targetID].insert(2, classRole + ' ' + message.author.name)
                                participantCount[targetID] += 1
                                yield from generateList(message, targetID,  '```diff\n+ {} has joined.```'.format(message.author.name))
                                appended = True
                                break
                            elif isinstance(EQTest[targetID][3], PlaceHolder):
                                EQTest[targetID].pop(2)
                                EQTest[targetID].insert(2, classRole + ' ' + message.author.name)
                                participantCount[targetID] += 1
                                yield from generateList(message, targetID,  '```diff\n+ {} has joined.```'.format(message.author.name))
                                appended = True
                                break
                        else:
                            yield from generateList(message, targetID, "```fix\nYou are already in the Party!```")
                            break
                        if not appended:
                            if personInMPA == False: 
                                yield from generateList(message, targetID, "```css\nThis party is full!```")
                                return
                            else:
                                yield from generateList(message, targetID, "```css\nYou are already in the Party```")
                        appended = False                                
            else:
                yield from client.delete_message(message)
        elif message.content.lower().startswith('%leave'):
            targetID = ''
            userstr = message.content
            userstr = userstr.replace("%leave", "")
            userstr = userstr.replace(" ", "")
            if userstr == '':
                yield from client.send_message(message.channel, 'Whose party are you trying to get out of?')
            elif userstr.startswith('<@'):
                if len(message.mentions) > 1:
                    yield from client.send_message(message.channel, 'You can only remove yourself from one party at a time!')
                    return
                elif message.mentions[0] != None:
                    targetID = message.mentions[0].id
            if message.author.top_role.permissions.send_tts_messages == True and message.channel.id == QuestChannelID:
                if targetID in EQTest:
                    yield from client.delete_message(message)
                    for index, item in enumerate(EQTest[targetID]):
                        if (type(EQTest[targetID][index]) is PlaceHolder):
                            pass
                        elif message.author.name in item:
                            EQTest[targetID].pop(index)
                            EQTest[targetID].insert(index, PlaceHolder(''))
                            participantCount[targetID] -= 1
                            yield from generateList(message, targetID, '```diff\n- Removed {} from the MPA list```'.format(message.author.name))
                            inMPA = True
                            return
                    if inMPA == False:
                        yield from generateList(message, targetID, '```fix\nYou were not in the Party list in the first place.```')
                elif targetID == '':
                    yield from client.delete_message(message)
                    yield from client.send_message(message.channel, 'Did you select the right person to remove yourself from?')
                    return
                else:
                    yield from client.send_message(message.channel, 'No party list found under that name.')
                    
        elif message.content.lower() == '%closept':
            if message.author.top_role.permissions.send_tts_messages == True and message.channel.id == QuestChannelID:
                if message.author.id in EQTest:
                    todelete = yield from client.get_message(message.channel, PTID[message.author.id])
                    try:
                        yield from client.delete_message(message)
                        del EQTest[message.author.id]
                        yield from client.delete_message(todelete)
                        del PTID[message.author.id]
                    except KeyError:
                        pass
                else:
                    yield from client.send_message(message.channel, 'There is no party to remove!')
            else:
                yield from client.send_message(message.channel, 'You can only use this command in the correct looking for party channel!')
        # Allows the party creator to add names to their own list.        
        elif message.content.lower().startswith('%add '):
            if message.author.top_role.permissions.send_tts_messages == True and message.channel.id == QuestChannelID:
                userstr = ''
                if message.author.id in EQTest:
                    userstr = message.content
                    userstr = userstr.replace("%add ", "")
                    targetID = message.author.id
                    if userstr == "":
                        yield from generateList(message, "```fix\nYou can't add nobody. Are you drunk?```")
                        appended = True
                    else:
                        for word in EQTest[message.author.id]:
                            if isinstance(word, PlaceHolder):
                                if not(userstr in EQTest[message.author.id]):
                                    if isinstance(EQTest[message.author.id][0], PlaceHolder):
                                        EQTest[message.author.id].pop(0)
                                        EQTest[message.author.id].insert(0, userstr)
                                        participantCount[message.author.id] += 1
                                        yield from generateList(message, targetID, '```diff\n+ Added {} to the party list```'.format(userstr))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.author.id][1], PlaceHolder):
                                        EQTest[message.author.id].pop(1)
                                        EQTest[message.author.id].insert(1, userstr)
                                        participantCount[message.author.id] += 1
                                        yield from generateList(message, targetID, '```diff\n+ Added {} to the party list```'.format(userstr))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.author.id][2], PlaceHolder):
                                        EQTest[message.author.id].pop(2)
                                        EQTest[message.author.id].insert(2, userstr)
                                        participantCount[message.author.id] += 1
                                        yield from generateList(message, targetID, '```diff\n+ Added {} to the party list```'.format(userstr))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.author.id][3], PlaceHolder):
                                        EQTest[message.author.id].pop(3)
                                        EQTest[message.author.id].insert(3, userstr)
                                        participantCount[message.author.id] += 1
                                        yield from generateList(message, targetID, '```diff\n+ Added {} to the party list```'.format(userstr))
                                        appended = True
                                        break
                    if not appended:
                        yield from generateList(message, "```css\nThe party is full!```")
                else:
                    yield from client.send_message(message.channel, 'You do not have a party to add someone to!')
                yield from client.delete_message(message)
            else:
                yield from client.send_message(message.channel, "You don't have permissions to use this command")  

        #Removes the player object that matches the input string that is given.
        elif message.content.lower().startswith('%remove'):
            if message.author.top_role.permissions.send_tts_messages == True and message.channel.id == QuestChannelID:
                if message.author.id in EQTest:
                    targetID = message.author.id
                    if len(EQTest[message.author.id]):
                            userstr = message.content
                            userstr = userstr.replace("%remove ", "")
                            for index in range(len(EQTest[message.author.id])):
                                appended = False
                                if (type(EQTest[message.author.id][index]) is PlaceHolder):
                                    pass
                                elif userstr.lower() in EQTest[message.author.id][index].lower():
                                    toBeRemoved = EQTest[message.author.id][index]
                                    EQTest[message.author.id][index] = userstr
                                    EQTest[message.author.id].remove(userstr)
                                    EQTest[message.author.id].insert(index, PlaceHolder(''))
                                    userstr = userstr
                                    participantCount[message.author.id] -= 1
                                    yield from generateList(message, targetID, '```diff\n- Removed {} from the party list```'.format(toBeRemoved))
                                    appended = True
                                    break
                            if not appended:    
                                yield from generateList(message, targetID, "```fix\nPlayer {} does not exist in the party list```".format(userstr))
                    else:
                        yield from client.send_message(message.channel, "Your party is empty! Dont go pretending that you have people in the party!")
                else:
                    yield from client.send_message(message.channel, 'There is no MPA.')
                yield from client.delete_message(message)
            else:
                yield from generateList(message, "You don't have permissions to use this command")
        # Restarts the bot. Bot owner only.        
        elif message.content.lower() == '%%restart':
            if message.author.id == ownerID:
                yield from client.send_message(message.channel, 'Tonk will now restart!')
                print ('The restart command was issued! Restarting Bot...')
                yield from client.change_presence(game=discord.Game(name='Restarting...'), status=discord.Status.idle)
                os.execl(sys.executable, *([sys.executable]+sys.argv))
            else:
                yield from client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
        # Shuts down the bot. Bot owner only.        
        elif message.content.lower() == '%%shutdown':
            if message.author.id == ownerID:
                yield from client.send_message(message.channel, 'Shutting down...')
                yield from client.logout()
            else:
                yield from client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
                
        # Allows a moderator to close another user's party.        
        elif message.content.lower().startswith('%close'):
            userstr = message.content
            userstr = userstr.replace("%close ", "")
            if userstr == '':
                yield from client.send_message(message.channel, 'Whose party are you trying to get out of?')
            elif userstr.startswith('<@'):
                if len(message.mentions) > 1:
                    yield from client.send_message(message.channel, 'You can only remove yourself from one party at a time!')
                    return
                elif message.mentions[0] != None:
                    targetID = message.mentions[0].id
            if message.author.top_role.permissions.manage_channels == True and message.channel.id == QuestChannelID:
                if targetID in EQTest:
                    todelete = yield from client.get_message(message.channel, PTID[targetID])
                    try:
                        yield from client.delete_message(message)
                        del EQTest[targetID]
                        yield from client.delete_message(todelete)
                        del PTID[targetID]
                    except KeyError:
                        print ("FAILED TO DELETE")
                else:
                    yield from client.send_message(message.channel, 'There is no party to remove!')
            else:
                yield from client.send_message(message.channel, 'You can only use this command in the correct looking for party channel!')

    
@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print ('Logged in to servers:')
    for item in client.servers:
        print (item)
    print('------')
client.run('token')