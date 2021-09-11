import pandas as pd
import numpy as np
import pyxel
import random




class App:
    def __init__(self,card_board_f,debug = True):
        self.width ,self.height = 200, 150
        self.caption = 'The Stars Are Right'
        pyxel.init(self.width,self.height,caption=self.caption)
        pyxel.load("assets/stars_and_btns.pyxres",True,False,False,False)
        pyxel.mouse(True)
        self.card_board_f = card_board_f
        self.board_x_gap = 0
        self.board_y_gap = 0
        self.board_right_shift = 0
        self.action = None
        self.debug = debug
        self.row_long = 4
        self.location_maping()
        self.board_cards = self.board_setting()
        pyxel.run(self.update, self.draw)

    def locate_mouse(self,x,y):
        # find if on boards
        if self.debug:
            print(x,y)
        for locate,location_screen in self.board_map.items():
            screen_x , screen_y = location_screen['x'],location_screen['y']
            if screen_x <= x <= (screen_x +16) and screen_y <= y <= screen_y +16:
                return locate
        # find if on btns

    def board_setting(self):
        result = ['2s'] * 7 + ['1s'] * 5 + ['vo'] * 3 + ['lm'] * 3 + ['ss'] * 3 + ['su'] * 2 + ['mo'] * 2
        # print(result)
        # result = [self.card_flip(card) if random.randint(0,1)==1 else card for card in result]
        random.shuffle(result)
        return result

    def location_maping(self):
        self.img_map = dict()
        img_name = ['su','se','4s','1s','ss','mt'
                   ,'mo','me','5s','vo','3s','2s','lm','gm'
                   ,'right','left','up','down'
                   ,'flip','switch','row_move','bl']
        img_loc = [{'x':x,'y':y} for y in range(0,16*11,16) for x in range(0,16*2,16)]        
        for name, loc in zip (img_name,img_loc):
            self.img_map[name] = loc
        
        self.c_name = ['Cthulhu','Tsatso','Hastur','Chaugnar'
                      ,'Dagoon','Ossadogowa',"Hastur's Spawn","Miri Nigri"
                      ,'Deep Ones', 'Formless', 'Byakhee', 'Tcho Tcho']
        img_loc = [{'x':x,'y':y} for x in range(32,32+32*3,32) for y in range(0,32*4,32)]        
        for name, loc in zip (self.c_name,img_loc):
            self.img_map[name] = loc

        minion = ['Gug', 'Tindaloo', 'Dhole', 'Ghast', 'Ghouls']
        minion_img_loc = [{'x':128,'y':y} for y in range(0,32*5,32)]        
        for name, loc in zip (minion,minion_img_loc):
            self.img_map[name] = loc
        self.c_name += minion


        self.board_map = dict()
        for x in range(5):
            for y in range(5):
                self.board_map[(x,y)] = ({'x':25+x*18,'y':30+y*18})
    
    def gap_reset(self):
        self.board_map = dict()
        for x in range(5):
            for y in range(5):
                self.board_map[(x,y)] = ({'x':25+x*(18+self.board_x_gap)+self.board_right_shift,'y':60+y*(18+self.board_y_gap)})

    def card_to_board(self,cards):
        if len(cards) <2:
            card = cards[0]
            self.board_x_gap = 0
            self.t_board = False
            self.board_right_shift = 0
        else:
            self.board_x_gap = 20 if len(cards)==2 else 3
            self.board_right_shift = 10 if len(cards)==2 else 0
            self.t_board = True
            card = []
            for c in cards:
                card += c
        self.gap_reset()
        res = []
        self.row_long = len(card[0])
        for l in card:
            for r in l:
                res.append(r)
        self.board_cards = res

    def board_draw(self,board_map_loc, img_loc,object_size={'wight':16,'height':16},shift_x=0,shift_y=0):
        """
        board_map_loc : tuple or int (int will transfer to  tuple)
        img_loc name of img : str
        object size : default 16 *16
        """
        if type(board_map_loc)==int:
            board_map_loc = (board_map_loc % self.row_long ,board_map_loc //self.row_long ,)
            if self.t_board:
                board_map_loc = board_map_loc[::-1]
        location_screen = self.board_map.get(board_map_loc)
        location_source = self.img_map.get(img_loc)
        if not location_screen and not location_source:
            print(f'{location_screen} or {location_source} not found')
            return
        try:
            pyxel.blt(location_screen['x'] + shift_x, location_screen['y'] + shift_y, 0
                     ,location_source['x'], location_source['y']
                     ,object_size['wight'], object_size['height'])
        except Exception as e:
            print(f'error :{e} , {board_map_loc}, {img_loc}')

    def card_draw(self,card_name,object_size={'wight':32,'height':32}):
        """
        object size : default 32*32
        """
        location_screen = {'x':45, 'y':25}
        location_source = self.img_map.get(card_name)
        if not location_screen and not location_source:
            print(f'{location_screen} or {location_source} {card_name} not found')
            return
        try:
            pyxel.blt(location_screen['x'] ,location_screen['y'] , 0
                     ,location_source['x'], location_source['y']
                     ,object_size['wight'], object_size['height'])
        except Exception as e:
            print(f'error :{e} , {card_name}')

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            self.trigger_shuffle = True
            self.trigger_wait = pyxel.frame_count +50        
            
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            x = pyxel.mouse_x
            y = pyxel.mouse_y
            click_board = self.locate_mouse(x,y)

    def draw(self):
        # base background
        pyxel.cls(13)
        pyxel.text(20,5, self.caption, 9)
        card_no = pyxel.frame_count//3 % 75
        cards = self.card_board_f[card_no]
        card_name = cards.get('card_name')
        pyxel.text(48,15, f'{card_name}', 9)
        if self.debug:
            pyxel.text(150,7, f'{pyxel.mouse_x,pyxel.mouse_y}', 9)
        y = 120
        for card in cards:
            pyxel.text(5,y,f'{card_no}, {card}',9)
            y +=10

        self.card_to_board(cards.get('card_board'))
        # draw main board
        for i in range(len(self.board_cards)):
            img_name = self.board_cards[i]
            self.board_draw(i,img_name)
        self.card_draw(card_name)
        

if __name__ == '__main__':
    df = pd.read_csv("./card_info.csv",names=['card_name','card_level','play_effect','bouns','card_type','points','summon_board','power'])
    arr = np.array(df)
    board_match = {'2' : '2s', '1' : '1s', 'V' : 'vo', 'Wn' : 'lm', 'Sh' : 'ss'
        , 'Su' : 'su', 'Mo' : 'mo', '3' : '3s'
        , '4' : '4s', '5' : '5s', 'Wx' : 'gm'
        , 'Me' : 'mt', 'So' : 'se', 'L' : 'me','b':'bl'}
    counter = 0
    card_board_f = dict()
    for card in arr:
        card_name = card[0]
        raw_board = card[-2]
        boards = raw_board.split('&')
        f_boards = []
        for board in boards:
            board = [[board_match[icon] for icon in l.split('-')] for l in board.split('/')]
            f_boards.append(board)
        card_board_f[counter] = {'card_name':card_name,'card_board':f_boards.copy()}
        counter +=1
    App(card_board_f,debug=True)
