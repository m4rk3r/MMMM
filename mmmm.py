import curses
import curses.textpad
import thread
import glob
#import pyaudio
import time
from random import choice,randrange
import logging
from graphics import text_map
logging.basicConfig(filename='debug.out',level=logging.DEBUG,)

#import psyco
#psyco.full()

# 86x35

"""
NOTES:
    - create templtes, render out text every step for new results (apperance of movement)
    - thread sound to interact with story
    - work in references + influences: http://en.wikipedia.org/wiki/Colossal_Cave_Adventure
    
TODO:
    - make maze/map
    - generate graphics for game
    /- sound
    /- (flesh out story)
    - top view map
    - sideview map
    ?- txtmode wipe transition
    /- title screen

IDEAS:
    - collect items that produce sound
    - think of sound output

    txt  = 'OREINT NOT PARALLEL \n'
    txt += 'direction: %s '% _dir
    txt +='\n orientation: %s' % fd
    txt +='\n position: %s '%str(self.position)
    txt +='\n moved_by: %s'%str([self.moves[_dir][0],self.moves[_dir][1]])
    logging.debug(txt)
"""

title_text = ''' __  __    _    ____ ___ ____   __  __    _  _____ ____  _____  __
|  \/  |  / \  / ___|_ _/ ___| |  \/  |  / \|_   _|  _ \|_ _\ \/ /
| |\/| | / _ \| |  _ | | |     | |\/| | / _ \ | | | |_) || | \  / 
| |  | |/ ___ \ |_| || | |___  | |  | |/ ___ \| | |  _ < | | /  \ 
|_|  |_/_/   \_\____|___\____| |_|  |_/_/   \_\_| |_| \_\___/_/\_\

 __  __ _____  _______ ____    __  __  ___  _   _ _   _ _____  _    ___ _   _ 
|  \/  |_ _\ \/ / ____|  _ \  |  \/  |/ _ \| | | | \ | |_   _|/ \  |_ _| \ | |
| |\/| || | \  /|  _| | |_) | | |\/| | | | | | | |  \| | | | / _ \  | ||  \| |
| |  | || | /  \| |___|  _ <  | |  | | |_| | |_| | |\  | | |/ ___ \ | || |\  |
|_|  |_|___/_/\_\_____|_| \_\ |_|  |_|\___/ \___/|_| \_| |_/_/   \_\___|_| \_|'''

cloud_shapes = ['''
    #####
 ###########
    ######
  ''',
  '''
    ##
#########
  ''',
'''
 ## ###
##########
''',
  
  '''
  ####
  ''',
  ]
  


graphics_folder = '/Users/mbeasl/programming/lampo/mmmm/elements/graphics/'
level_folder    = '/Users/mbeasl/programming/lampo/mmmm/elements/level/'
boolean_map = {'False':'Undiscovered','True':'Found'}


class Graphics:
    def __init__(self):
        self.graphics_bin = self.index_graphics(graphics_folder)
        self.level_bin   = self.index_graphics(level_folder)
        
    def render_template(self,graphic_bin,key):
        """ print self.render_template(self.graphics,'mountain') """
        element = graphic_bin[key]
        formated = []
        for row in element:
            tmp = []
            for i in range(len(row)):
                if row[i] != '\n':
                    opt = text_map[key][row[i]]
                    if type(opt)==tuple: 
                        new_char = choice(opt)
                    elif type(opt)==list:
                        new_char = opt[0]
                        tmp_item = text_map[key][row[i]].pop(0)
                        text_map[key][row[i]].append(tmp_item)
                    else: 
                        new_char = opt
                else:
                    new_char = ' '
                tmp.append(new_char)
            formated.append(tmp)
        return formated
        

    def index_graphics(self,dir):
        items = glob.glob(dir+'*.txt')
        dic = {}
        for item in items:
            name = item.split('/')[-1].split('.')[0]
            dic[name]= open(item).readlines()
        return dic
        
    def render(self,screen,template,dim):
        for y in range(len(template)-1):
            for x in range(len(template[0])-1):
                screen.addstr(y,x,template[y][x]) # add color

############
## SOUND  ##
############

class Sound:
    def __init__(self,parent):
        self.parent = parent
        self.CHUNK = 1024
        self.FORMAT ='' #pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 24100
        self.p = pyaudio.PyAudio()
        self.active = True
        self.stage = 0
        self.audio_bin = []
        thread.start_new(self.render_audio,())
        #self.render_audio()
        self.sound_stages = [
                [   # highest
                    [100000,10,' '],
                    [100000,40,' '],
                    #[90000,80,' '],
                    #[100000,5,' '],
                ],
                [
                    [80000,100,' '],
                    [90000,400,' '],
                    #[80000,800,' '],
                    #[70000,1000,' '],
                ],
                [
                    [20000,100,''],
                    [90000,400,''],
                    #[8000,800,''],
                    #[7000,1000,''],
                ],
                [
                    [50000,900,' '],
                    [30000,600,' '],
                    #[2000,400,' '],
                    #[1000,100,' '],
                ],
                [
                    [20000,150,' '],
                    [15000,100,' '],
                    #[1000,20,' '],
                    #[1000,10,' '],                
                ],            
            ]
            
    def play_token(self):
        z=4000
        for t in txt:
            print t,
            stream.write(t,z)
        
    
    def set_new_stage(self,stage):
        self.stage = stage
        self.stagger()
    
    def stagger(self):
        for item in self.sound_stages[self.stage]:
            if randrange(0,3) == 2: self._kill_audio_stage(item[2])
            self.create_stream(item[0],item[1],item[2])
            #time.sleep(randrange(0,3))
        
    def create_stream(self,rate=48000,chunk=1024,data=''):
        tmp = [
                    self.p.open(format =self.FORMAT, channels =self.CHANNELS,
                    rate = rate, input = False, output = True),
                    data,
                    chunk,
                    self.stage,
              ]
        self.audio_bin.append(tmp)
    
    def _kill_audio_stage(self,stage):
            for x in range(len(self.audio_bin)):
                if self.audio_bin[x][3] != stage:
                    self.kill_audio(index=x)
                    break
        
    def kill_audio(self,index = 0):
        self.audio_bin[index][0].stop_stream()
        self.audio_bin[index][0].close()
        del self.audio_bin[index]
        
    def render_audio(self):
        while self.active:
            for stream in self.audio_bin:
                stream[0].write(stream[1],stream[2])
            time.sleep(0.0000001)

class Player:
    def __init__(self,parent):
        self.parent = parent
        self.inventory = {
            'a':False,
            'b':False,
            'c':False,
            'd':False,
            'e':False,
            'f':False,
            'g':False,
        }
        self.foothill_names = {
            'a': "North Foothill",
            'b': "North-East Foothill",
            'c': "East Foothill",
            'd': 'South Foothill',
            'e': 'South-West Foothill',
            'f': 'West Foothill',
            'g': 'South-East Foothill',
        }
        
        self.face_dir = 1
        
        position  = []
        self.state = False
        self.dim = self.parent.dim
        self.inv_dim = (30,40)
        self.inventory_ui = curses.newwin(self.inv_dim[0],self.inv_dim[1]+1,2,30)
        
    def show_inventory(self):
        self.inventory_ui.clear()
        for y in range(self.inv_dim[0]):
            for x in range(self.inv_dim[1]):
                if y == 0 and x == 0: 
                    self.inventory_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == 0 and x == self.inv_dim[1]-1: 
                    self.inventory_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == self.inv_dim[0]-1 and x == 0: 
                    self.inventory_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == self.inv_dim[0]-1 and x == self.inv_dim[1]-1: 
                    self.inventory_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == 0:
                    self.inventory_ui.addstr(y,x,"-",curses.color_pair(0))
                elif y == self.inv_dim[0]-1:
                    self.inventory_ui.addstr(y,x,"-",curses.color_pair(0))
                elif x == 0 or x == self.inv_dim[1]-1:
                    self.inventory_ui.addstr(y,x,"|",curses.color_pair(0))
        self.inventory_ui.addstr(1,1,'INVENTORY')        
        y=3
        for item in self.inventory.keys():
            self.inventory_ui.addstr(y,3,self.foothill_names[item])
            self.inventory_ui.addstr(y,26,boolean_map[str(self.inventory[item])])
            y+=1
            # if I have time draw pieces 
        self.inventory_ui.overwrite(self.parent.screen)        
                    
                
                
class Level:
    def __init__(self,parent):
        self.parent = parent
        self.labyrinth = []
        self.foothills = []
        self.foothill_items = {}
        self.dim = self.parent.dim
        self.map_dim = [33,84]
        self.map_ui = curses.newwin(self.map_dim[0],self.map_dim[1]+1,0,0) #(self.dim[0]/2-self.map_dim[0]/2),(self.dim[1]/2-self.map_dim[1]/2))
        fy,fx = 20,35
        self.foot_dim = [20,35]
        self.foothill_ui = curses.newwin(self.foot_dim[0],self.foot_dim[1],5,10) #(self.dim[0]/2- fy/2),(self.dim[1]/2 - fx/2))
        self.position = [8,0]
        self.moves = {
            'up':    [-1,0],
            'down':  [1,0],
            'left':  [0,-1],
            'right': [0,1],
        }
        self.raw_map = open(level_folder+'map.txt').readlines()
        self.raw_vmap = ''#open(level_folder+'vmap.txt').readlines()
        self.map = []
        self.v_map = []
        self.build()
        self.current = [0,0]
        self.get_foothill_items()
        self.new_audio = False
        
        self.foothill_names = {
            'a': "North Foothill",
            'b': "North-East Foothill",
            'c': "East Foothill",
            'd': 'South Foothill',
            'e': 'South-West Foothill',
            'f': 'West Foothill',
            'g': 'South-Eas Foothill',
        }
        
    def build(self):
        y=0
        x=0
        for row in self.raw_map:
            _r = []
            x=0
            for col in list(row.strip('\n')):
                if col in ['a','b','c','d','e','f','g']:
                    self.foothills.append([y,x])
                    _r.append(col)
                else:
                    _r.append(int(col))
                x+=1
            y+=1
            self.map.append(_r)
        if self.raw_vmap:
            pass
    
    def get_foothill_items(self):
        items = glob.glob(graphics_folder+'*.txt')
        for item in items:
            key = item.split('_')[1].replace('.txt','')
            txt = open(item).readlines()
            tmp = []
            for t in txt:
                tmp.append(list(t))
            self.foothill_items[key]=tmp

    
    def foothill_token(self,key):
        token = self.foothill_items[key]    
        self.foothill_ui.addstr(1,10,self.foothill_names[key])
        if not self.new_audio:
            try:
                self.parent.sound.set_new_stage(randrange(0,5))
                self.new_audio = True
            except:
                pass
            #logging.debug(self.parent.sound.audio_bin)

        for y in range(len(token)):
            for x in range(len(token[y])):
                self.foothill_ui.addstr(y+6,x+6,token[y][x])
        
        for y in range(self.foot_dim[0]-1):
            for x in range(self.foot_dim[1]):
                if y == 0 and x == 0: 
                    self.foothill_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == 0 and x == self.foot_dim[1]-1: 
                    self.foothill_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == self.foot_dim[0]-2 and x == 0: 
                    self.foothill_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == self.foot_dim[0]-2 and x == self.foot_dim[1]-1: 
                    self.foothill_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == 0:
                    self.foothill_ui.addstr(y,x,"-",curses.color_pair(0))
                elif y == self.foot_dim[0]-2:
                    self.foothill_ui.addstr(y,x,"-",curses.color_pair(0))
                elif x == 0 or x == self.foot_dim[1]-1:
                    self.foothill_ui.addstr(y,x,"|",curses.color_pair(0))
        self.parent.player.inventory[key] = True
        self.foothill_ui.overwrite(self.parent.screen)
        
    def show_map(self):
        #self.map_dim[0] = len(self.map)
        #self.map_dim[1] = len(self.map[0])
        for y in range(self.map_dim[0]):
            for x in range(self.map_dim[1]):
                if y == 0 and x == 0: 
                    self.map_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == 0 and x == self.map_dim[1]-1: 
                    self.map_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == self.map_dim[0]-1 and x == 0: 
                    self.map_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == self.map_dim[0]-1 and x == self.map_dim[1]-1: 
                    self.map_ui.addstr(y,x,"+",curses.color_pair(0))
                elif y == 0:
                    self.map_ui.addstr(y,x,"-",curses.color_pair(0))
                elif y == self.map_dim[0]-1:
                    self.map_ui.addstr(y,x,"-",curses.color_pair(0))
                elif x == 0 or x == self.map_dim[1]-1:
                    self.map_ui.addstr(y,x,"|",curses.color_pair(0))
        self.map_ui.addstr(1,1,'MAP')        
        
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                opt = text_map['map'][self.map[y][x]]
                if type(opt)==tuple: 
                    new_char = choice(opt)
                elif type(opt)==list:
                    new_char = opt[0]
                    tmp_item = text_map['map'][self.map[y][x]].pop(0)
                    text_map['map'][self.map[y][x]].append(tmp_item)
                else: 
                    new_char = opt
                self.map_ui.addstr(y+1,x+1,new_char,curses.color_pair(3))
                
        avatar={'1':'>','2':'v','3':'<','0':'^'}
        self.map_ui.addstr(self.position[0]+1,self.position[1]+1,avatar[str(self.parent.player.face_dir)],curses.color_pair(4))
        self.map_ui.overwrite(self.parent.screen)
        
    def render_top_map(self):
        pass
        
    def render_side_map(self):
        pass
        
    def move(self,_dir,fd):
        
        
        if self.map[ (self.position[0] + self.moves[_dir][0]) ][self.position[1]]:
            self.current[0] = self.position[0]
            self.position[0] += self.moves[_dir][0]
        if self.map[self.position[0]][ (self.position[1] + self.moves[_dir][1]) ]:
            self.current[1] = self.position[1]
            self.position[1] += self.moves[_dir][1]

        
        if self.parent.player.face_dir==1:
            left = self.map[self.position[0]-1][self.position[1]]
            straight = self.map[self.position[0]][self.position[1]+1]
            right = self.map[self.position[0]+1][self.position[1]]
        elif self.parent.player.face_dir==0:
            left = self.map[self.position[0]][self.position[1]-1]
            straight = self.map[self.position[0]-1][self.position[1]]
            right = self.map[self.position[0]][self.position[1]+1]
        elif self.parent.player.face_dir==2:
            left = self.map[self.position[0]][self.position[1]+1]
            straight = self.map[self.position[0]+1][self.position[1]]
            right = self.map[self.position[0]][self.position[1]-1]
        elif self.parent.player.face_dir==3:
            left = self.map[self.position[0]+1][self.position[1]]
            straight = self.map[self.position[0]][self.position[1]-1]
            right = self.map[self.position[0]-1][self.position[1]]
        
        #logging.debug(self.map[self.position[0] + self.moves[_dir][0]][self.position[1]])
        
        if self.map[ (self.position[0] + self.moves[_dir][0]) ][self.position[1]] in ['a','b','c','d','e','f','g']  or \
        self.map[self.position[0]][ (self.position[1] + self.moves[_dir][1]) ] in ['a','b','c','d','e','f','g']:
            options = [0,(self.map[self.position[0]][ (self.position[1] + self.moves[_dir][1]) ]),0]
        else:
            options = [left, straight, right]        
        
        #logging.debug(str(self.position))
        return self.position,options,self.current
            



class Mountain:
    def __init__(self):
        self.screen = curses.initscr()
        self.dim = self.screen.getmaxyx()
        self.title = curses.newwin(10,self.dim[1]+60,0,0)
        self.position_ui = curses.newwin(10,self.dim[1]+60,0,0)
        self.title_text = curses.newwin(11,80, 2,3)
        
        # colors
        curses.start_color()
        bg = curses.COLOR_BLACK
        curses.init_pair(1, curses.COLOR_BLUE, bg)
        curses.init_pair(2, curses.COLOR_CYAN, bg)
        curses.init_pair(3, curses.COLOR_GREEN, bg)
        curses.init_pair(4, curses.COLOR_MAGENTA, bg)
        curses.init_pair(5, curses.COLOR_RED, bg)
        curses.init_pair(6, curses.COLOR_YELLOW, bg)
        
        #coords
        self.top = 0
        self.left = 0
        curses.noecho()
        self.screen.nodelay(1)
        
        # init classes
        self.graphics = Graphics()
        self.sound    = Sound(self)
        self.player   = Player(self)
        self.level    = Level(self)
        
        # start sound
        #self.sound.set_new_stage(1)
        
        # fetch inital template
        self.template = self.graphics.render_template(self.graphics.level_bin, 'mountain')
        self.options = [0,1,0]
        
        # control states
        self.state = {
            'title': True,
            'inventory': False,
            'vmap': False,
            'map': False,
        }
        self.keymap = {
            'w' : ['up','right','down','left'],
            's' : ['down','left','up','right'],
            'd' : ['right','down','left','up'],
            'a' : ['left','up','right','down'],
        }
        
        self.pos = [0,0]
        self.current = [0,0]
        self.cloud = []
        self.sound_started = False
        
        for x in range(20):
            mv = randrange(randrange(3,15),20)
            mx = randrange(0,40)
            self.cloud.append([curses.newwin(10,15,0,0),mv,mx])
            self.cloud[x][0].addstr(0,0,choice(cloud_shapes))
            self.cloud[x][0].overlay(self.screen)
        
        self.timer = 0
        # start
        self.main()
        
        
    def render_end(self):
        pass
        
    
    def textbox_edit(self,key):
        if key != -1:
            if key == 10:
                print self.text_input.gather()
                self.edit = False
    
    def main(self):
        #curses.halfdelay(1) 
        while 1:
            c=self.screen.getch()
            if c==ord('q'):
                self.screen.keypad(0)
                curses.echo()
                curses.nocbreak()
                curses.endwin()
                break
            elif c==ord('i'):
                self.state['title']=False
                self.state['inventory'] = not self.state['inventory']
            elif c==ord('m'):
                self.state['title']=False
                self.state['map'] = not self.state['map']
            elif c==ord('d'):
                self.state['title']=False
                self.player.face_dir = (self.player.face_dir + 1)%4
                #self.pos = self.level.move(self.keymap['d'][self.player.face_dir],self.player.face_dir)
            elif c == ord('a'): 
                self.state['title']=False
                self.player.face_dir = (self.player.face_dir - 1)%4
                #self.pos = self.level.move(self.keymap['a'][self.player.face_dir],self.player.face_dir)
            elif c == ord('w'): 
                self.state['title']=False
                #self.player.face_dir = (self.player.face_dir - 1)%4
                self.pos,self.options,self.current = self.level.move(self.keymap['w'][self.player.face_dir],self.player.face_dir)
                self.template = self.graphics.render_template(self.graphics.level_bin, '%s_%s_%s'%tuple(self.options))
                #logging.debug(str(self.pos)+"/\/\/\/"+ str(self.level.foothills))
                logging.debug(self.level.foothills)
            elif c == ord('s'): 
                pass
                #self.player.face_dir = (self.player.face_dir - 1)%4
                #self.pos = self.level.move(self.keymap['s'][self.player.face_dir],self.player.face_dir)
                

            #################
            ## GAME STATES ##
            #################
            
            self.graphics.render(self.screen,self.template,self.dim)

            self.position_ui.addstr(0, 0,"position: %s"%str(self.pos),curses.color_pair(3))
            self.position_ui.overlay(self.screen)


            if self.state['title']:
                self.template = self.graphics.render_template(self.graphics.level_bin, 'mountain')

                # title
                self.title_text.addstr(0,0,title_text,curses.color_pair(3))
                self.title_text.overwrite(self.screen)

                self.timer+=1
                for c in self.cloud:
                    if self.timer%5==0:
                        c[2] += 1
                        
                    if c[2]+20 > self.dim[1]:
                        c[2] = 0
                        c[1] = randrange(randrange(5,10),20)
                        c[2] = 0#randrange(-2,86)
                    try:
                        c[0].mvwin(c[1],c[2])
                    except:
                        pass
                    c[0].overlay(self.screen)


                self.screen.refresh()
                curses.napms(15)
            else: 
                if not self.sound_started:
                    try:
                        self.sound.set_new_stage(1)
                        self.sound_started = True
                    except:
                        pass
                
                #self.title.addstr(2, self.left,"MAGIC MATRIX MIXER MOUNTAIN",curses.color_pair(randrange(0,6)))
                #self.title.overlay(self.screen)
                #self.left +=1
                #if self.left > self.dim[1]:
                #    self.left = 0
                self.title.clear()
            
            if self.state['inventory']:
                self.player.show_inventory()
                
            if self.state['map']:
                self.level.show_map()


            if self.pos in self.level.foothills:
                #try:
                self.level.foothill_token(self.options[1])            
                #except:
                #    pass
            else:
                self.level.new_audio = False

            
Mountain()


""" tests """
#gr = Graphics()
#tmp = gr.render_template(gr.level_bin,'0_1_0')
#print tmp
#gr.render(None, tmp, None)

#lv = Level()

#sound relationship... slower rate/ greater chunk - more vacumus
# floor 1000, ceiling 200000
#sn = Sound()
#sn.create_stream(rate=1000,chunk=20,data=' ')
#sn.create_stream(rate=100000,chunk=10,data='')
#x = [
#[2000,150,' '],
#[1500,100,' '],
#[1000,20,' '],
#[1000,10,' '],
#]
#for z in x:
#    sn.create_stream(z[0],z[1],z[2])
#sn.render_audio()