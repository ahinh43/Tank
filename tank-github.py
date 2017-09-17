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
MPATitle = {}
activePT = {}
PTauthor = {}
PTmention = {}
PTID = {}
participantCount = {}
appended = False
client = discord.Client()
getTime = datetime.now()

# Load all the quest channels in the array
with open("questchannels.txt") as f:
    questChannels = f.readlines()
    

@asyncio.coroutine
def generateList(message, targetID, inputstring):
    pCount = 1
    nCount = 1
    mpaCount = 1
    alreadyWroteList = False
    ptleader = yield from client.get_user_info(targetID)
    playerlist = '\n'
    for word in EQTest[targetID]: 
        if nCount == 1:
            mpaCount += 1
        if (type(word) is PlaceHolder):
            playerlist += ('**>** ' + '\n')
        else:
            playerlist += ('**>** ' + " " + word + '\n')
        pCount+=1
        nCount+=1
        if nCount == 5:
            playerlist += ('\n')
            nCount = 1
        #em = discord.Embed(description='**Party Name: **' + '\t' + '**Party status: **' + str(participantCount[targetID]) + '/' + '4' + '\n' + MPATitle[targetID] + '\n' + '**Join this party by typing `%join @{}`** \n'.format(PTauthor[targetID]) + playerlist + inputstring, colour=0xB3ECFF)
        em = discord.Embed(description='Click on 📥 to join and 📤 to leave. If you are the party leader, use ❌ to close your party when you are done.', colour=0xB3ECFF)
        em.add_field(name='Party Name', value=MPATitle[targetID], inline=True)
        em.add_field(name='Party Status', value='`' + str(participantCount[targetID]) + '/' + '4 `', inline=True)
        em.add_field(name='Party Leader', value='`' + ptleader.name + '`', inline=True)
        em.add_field(name='Participant List', value=playerlist, inline=False)
        em.add_field(name='Last Action', value=inputstring, inline=False)
    try:
        yield from client.edit_message(EQPostDict[targetID], '', embed=em)
    except:
        EQPostDict[targetID] = yield from client.send_message(message.channel, '', embed=em)

            
@client.event
@asyncio.coroutine
def on_message(message):
    global questChannels
    PREFIX = '%'
    if message.content.startswith(PREFIX):
        if message.content.lower().startswith(PREFIX + 'creatept'):
            userstr = message.content
            userstr = userstr.replace(PREFIX + "creatept", "")
            if not message.author.id in EQTest:
                #if message.channel.id in questChannels:
                if message.author.top_role.permissions.send_tts_messages == True:
                    if userstr == '':
                        yield from client.send_message(message.channel, 'Your party must have a name! Use **{}creatept *<name>*** to properly create one!'.format(PREFIX))
                        return
                    EQTest[message.author.id] = list()
                    targetID = message.author.id
                    participantCount[message.author.id] = 0
                    for index in range(4):
                        EQTest[message.author.id].append(PlaceHolder(""))
                    if userstr.lower().startswith(' taco') or userstr.lower().startswith(' ta'):
                        for index in range(len(message.server.roles)):
                            if message.server.id == '':
                                if (message.server.roles[index].id == '333343210162356226'):
                                    yield from client.send_message(message.channel, '{} Time attack party!'.format(message.server.roles[index].mention))
                    elif userstr.lower().startswith(' aq') or userstr.lower().startswith(' lq') or userstr.lower().startswith('leveling'):
                        for index in range(len(message.server.roles)):
                            if message.server.id == '':
                                if (message.server.roles[index].id == '334071765053603850'):
                                    yield from client.send_message(message.channel, '{} EXP/Leveling party!'.format(message.server.roles[index].mention))
                    MPATitle[message.author.id] = userstr
                    PTauthor[message.author.id] = message.author.name
                    activePT[message.author.id] = True
                    yield from client.delete_message(message)
                    if isinstance(EQTest[targetID][0], PlaceHolder):
                        EQTest[targetID].pop(0)
                        EQTest[targetID].insert(0, message.author.name)
                        participantCount[targetID] += 1
                        yield from generateList(message, targetID, '```dsconfig\nStarting party! Please react to the green icon to sign up!```'.format(PREFIX, message.author.name, message.author.discriminator))
                    log = yield from client.logs_from(message.channel, limit=3, after=message)
                    for message in log:
                        if message.author.id == client.user.id:
                            PTID[targetID] = message.id
                            PTmention[targetID] = ''
                            break
                    for message in log:
                        if message.content.startswith('<@&333343210162356226>'):
                            PTmention[targetID] = message.id
                            break
                        elif message.content.startswith('<@&334071765053603850>'):
                            PTmention[targetID] = message.id
                            break
                    msg = EQPostDict[targetID]
                    yield from client.add_reaction(msg, '📥')
                    yield from client.add_reaction(msg, '📤')
                    yield from client.add_reaction(msg, '❌')
                    def check(reaction, user):
                        if user == client.user:
                            return
                        e = str(reaction.emoji)
                        return e.startswith(('📥', '📤', '❌'))
                    while activePT[targetID] == True:
                        res = yield from client.wait_for_reaction(message=msg, check=check)
                        inMPA = False
                        personInMPA = False
                        if res.reaction.emoji == '📥':
                            for index, item in enumerate(EQTest[targetID]):
                                if (type(EQTest[targetID][index]) is PlaceHolder):
                                    pass
                                elif res.user.name in item:
                                    personInMPA = True
                                    break
                                for word in EQTest[targetID]:
                                    if isinstance(word, PlaceHolder):
                                        if res.user.name in EQTest[targetID]:
                                            personInMPA = True
                                            break
                                        if personInMPA == False:
                                            if isinstance(EQTest[targetID][0], PlaceHolder):
                                                EQTest[targetID].pop(0)
                                                EQTest[targetID].insert(0, res.user.name)
                                                participantCount[targetID] += 1
                                                yield from generateList(message, targetID, '```diff\n+ {} has joined.```'.format(res.user.name))
                                                appended = True
                                                personInMPA = True
                                                break
                                            elif isinstance(EQTest[targetID][1], PlaceHolder):
                                                EQTest[targetID].pop(1)
                                                EQTest[targetID].insert(1, res.user.name)
                                                participantCount[targetID] += 1
                                                yield from generateList(message, targetID,  '```diff\n+ {} has joined.```'.format(res.user.name))
                                                appended = True
                                                personInMPA = True
                                                break
                                            elif isinstance(EQTest[targetID][2], PlaceHolder):
                                                EQTest[targetID].pop(2)
                                                EQTest[targetID].insert(2, res.user.name)
                                                participantCount[targetID] += 1
                                                yield from generateList(message, targetID,  '```diff\n+ {} has joined.```'.format(res.user.name))
                                                appended = True
                                                personInMPA = True
                                                break
                                            elif isinstance(EQTest[targetID][3], PlaceHolder):
                                                EQTest[targetID].pop(2)
                                                EQTest[targetID].insert(2, res.user.name)
                                                participantCount[targetID] += 1
                                                yield from generateList(message, targetID,  '```diff\n+ {} has joined.```'.format(res.user.name))
                                                appended = True
                                                personInMPA = True
                                                break
                                        if not appended:
                                            if personInMPA == False: 
                                                yield from generateList(message, targetID, "```css\nThis party is full!```")
                                                break
                                            else:
                                                yield from generateList(message, targetID, "```css\nYou are already in the Party```")
                                            appended = False
                            yield from client.clear_reactions(msg)
                            yield from client.add_reaction(msg, '📥')
                            yield from client.add_reaction(msg, '📤')
                            yield from client.add_reaction(msg, '❌')
                        elif res.reaction.emoji == '📤':
                            if targetID in EQTest:
                                for index, item in enumerate(EQTest[targetID]):
                                    if (type(EQTest[targetID][index]) is PlaceHolder):
                                        pass
                                    elif res.user.name in item:
                                        EQTest[targetID].pop(index)
                                        EQTest[targetID].insert(index, PlaceHolder(''))
                                        participantCount[targetID] -= 1
                                        yield from generateList(message, targetID, '```diff\n- Removed {} from the MPA list```'.format(res.user.name))
                                        inMPA = True
                                        break
                                if inMPA == False:
                                    yield from generateList(message, targetID, '```fix\nYou were not in the Party list in the first place.```')
                            yield from client.clear_reactions(msg)
                            yield from client.add_reaction(msg, '📥')
                            yield from client.add_reaction(msg, '📤')
                            yield from client.add_reaction(msg, '❌')
                        elif res.reaction.emoji == '❌':
                            if res.user.id == targetID or res.user.top_role.permissions.manage_channels == True:
                                try:
                                    yield from client.delete_message(msg)
                                    del EQTest[targetID]
                                    del PTID[targetID]
                                    del MPATitle[targetID]
                                    del PTauthor[targetID]
                                    del activePT[targetID]
                                    return
                                except KeyError:
                                    print ("FAILED TO DELETE")
                            else:
                                yield from generateList(message, targetID, '```fix\nOnly the party leader can delete the party!```')
                                yield from client.clear_reactions(msg)
                                yield from client.add_reaction(msg, '📥')
                                yield from client.add_reaction(msg, '📤')
                                yield from client.add_reaction(msg, '❌')
                            
                else:
                    yield from client.send_message(message.channel, 'You do not have the permissions to start parties!')
                #else:
                    #yield from client.send_message(message.channel, 'You are not in the right channel!')
            else:
                targetID = message.author.id
                yield from generateList(message, targetID, '```fix\nYou already have a party list being made!```')
                yield from client.delete_message(message)
        # Allows the party creator to add names to their own list.        
        elif message.content.lower().startswith(PREFIX + 'add '):
          #  if message.channel.id == '206673616060940288' or message.channel.id in questChannels:
            if message.author.top_role.permissions.send_tts_messages == True:
                userstr = ''
                if message.author.id in EQTest:
                    userstr = message.content
                    userstr = userstr.replace(PREFIX + "add ", "")
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
           # else:
             #   yield from client.send_message(message.channel, "You don't have permissions to use this command")  

        #Removes the player object that matches the input string that is given.
        elif message.content.lower().startswith(PREFIX + 'remove'):
          #  if message.channel.id == '206673616060940288' or message.channel.id in questChannels:
            if message.author.top_role.permissions.send_tts_messages == True:
                if message.author.id in EQTest:
                    targetID = message.author.id
                    if len(EQTest[message.author.id]):
                            userstr = message.content
                            userstr = userstr.replace(PREFIX + "remove ", "")
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
           # else:
              #  yield from generateList(message, "You don't have permissions to use this command")
        # Restarts the bot. Bot owner only.        
        elif message.content.lower() == '%%restart':
            if message.author.id == '':
                yield from client.send_message(message.channel, 'Tank will now restart!')
                print ('The restart command was issued! Restarting Bot...')
                yield from client.change_presence(game=discord.Game(name='Restarting...'), status=discord.Status.idle)
                os.execl(sys.executable, *([sys.executable]+sys.argv))
            else:
                yield from client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
                
                
        # Restarts the bot. Bot owner only.        
        elif message.content.lower() == '%%printchannels':
            if message.author.id == '':
                for word in questChannels:
                    print (word)
                
        # Shuts down the bot. Bot owner only.        
        elif message.content.lower() == '%%shutdown':
            if message.author.id == '':
                yield from client.send_message(message.channel, 'VROOOM AAAARR-')
                yield from client.logout()
            else:
                yield from client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
                
        elif message.content.lower() == PREFIX + 'help':
            em = discord.Embed(description='', colour=0xB3ECFF)
            em.add_field(name='Party Creator Commands', value='Commands for party creators:', inline=False)
            em.add_field(name=PREFIX + 'creatept <partyname>', value='**Replace**: <partyname> with the party name of your choice. \nCreates a party list. If the title starts with `taco`, `aq`, `leveling`, or `lq`, certain roles will be mentioned. You can only have one party at a time. Use `{}closept` when you are done to create a new one.'.format(PREFIX), inline=False)
            em.add_field(name=PREFIX + 'add <name>', value='**Replace**: <name> with a name of your choice. \nManually adds the name into the list. ', inline=False)
            em.add_field(name=PREFIX + 'remove <name>', value='**Replace**: <name> with the name on the list you want to remove. \nRemoves the name from your party list. If the name has a special character just copy and paste the name.', inline=False)
            #em.add_field(name=PREFIX + 'closept', value='Closes your party and removes the list. You should use this when you are finished with your party.', inline=False)
            #em.add_field(name='Party Member Commands', value='Commands for those joining parties:', inline=False)
            #em.add_field(name=PREFIX + '', value='**Replace**: @<name> with a name of your choice. \nJoins the mentioned persons party list if there is one. ', inline=False)
            #em.add_field(name=PREFIX + 'leave @<name>', value='**Replace**: @<name> with a name of your choice. \nLeaves the party of the name you mentioned. ', inline=False)
            #em.add_field(name=PREFIX + 'Server Moderator Commands', value='Commands for server moderators:', inline=False)
            #em.add_field(name=PREFIX + 'close @<name>', value='**Replace**: @<name> with a name of your choice. \nForce closes the party of the mentioned name. ', inline=False)
            em.set_author(name='All Tank Comamnds!')
            yield from client.send_message(message.channel, '', embed=em)
            
        #Reload the doggo memes
        elif message.content.lower() == PREFIX + 'reload channels':
            if message.author.id == '' or message.author.top_role.permissions.manage_channels:
                if not message.channel.name.startswith('mpa'):
                    del questChannels[:]
                    with open("questchannels.txt") as f:
                        questChannels = f.readlines()
                    yield from client.send_message(message.channel, 'Reloaded quest channels!')
        #Reload the doggo memes
        elif message.content.startswith(PREFIX + 'addchannel'):
            if message.author.id == '' or message.author.top_role.permissions.manage_channels:
                userstr = message.content
                userstr = userstr.replace(PREFIX + "addchannel ", "")
                userstr = userstr.replace(" ", "")
                if len(userstr) == 18 and type(client.get_channel(userstr)) != None:
                    with open("questchannels.txt", 'a') as f:
                        f.write('\n' + userstr)
                    del questChannels[:]
                    with open("questchannels.txt") as f:
                        questChannels = f.readlines()
                    yield from client.send_message(message.channel, 'Added the quest channel!')
                else:
                    yield from client.send_message(message.channel, 'Must be a channel ID to add!')
                    
                    
        elif message.content.lower().startswith('%%eval'):
            if message.author.id == '':
                userstr = message.content
                userstr = userstr.replace("%%eval", "")
                try:
                    result = eval(userstr)
                except Exception:
                    formatted_lines = traceback.format_exc().splitlines()
                    yield from client.send_message(message.channel, 'Failed to Evaluate.\n```py\n{}\n{}\n```'.format(formatted_lines[-1], '/n'.join(formatted_lines[4:-1])))
                    return

                if asyncio.iscoroutine(result):
                    result = yield from result

                if result:
                    yield from client.send_message(message.channel, 'Evaluated Successfully.\n```{}```'.format(result))
                    return
            else:
                yield from client.send_message(message.channel, 'No.')
        
                
@client.event
@asyncio.coroutine
def on_server_join(server):
    yield from client.send_message(client.get_channel('322466466479734784'), '```diff\n+ Joined {} ```'.format(server.name) + '(ID: {})'.format(server.id))
@client.event
@asyncio.coroutine
def on_server_remove(server):
    yield from client.send_message(client.get_channel('322466466479734784'), '```diff\n- Left {} ```'.format(server.name) + '(ID: {})'.format(server.id))
    
@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print ('Logged in to servers:')
    for item in client.servers:
        print (item)
    print ('Tank is now ready')
    print('------')
    yield from client.change_presence(game=discord.Game(name='just tank things'), status=discord.Status.online)                 
client.run('key')