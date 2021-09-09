import pyxel
import random
class App:
    def __init__(self):
        self.width ,self.height = 200, 150
        self.caption = 'The Stars Are Right'
        pyxel.init(self.width,self.height,caption=self.caption)
        pyxel.load("assets/stars_and_btns.pyxres",True,False,False,False)
        pyxel.mouse(True)
        self.action = None
        self.tmp = None
        self.trigger_shuffle = False
        self.color_match = {'flip':15, 'switch':11, 'row_move':8}
        self.highlight_dict = {col:set() for col in self.color_match.values()}
        self.fade_frame_count = 12
        self.fade_out = dict()
        self.location_maping()
        self.board_cards = self.board_setting()
        pyxel.run(self.update, self.draw)

    def card_flip(self,card_code):
        tmp = zip(['su','se','4s','1s','ss','mt','mo','me','5s','vo','3s','2s','lm','gm']
                  ,['se','su','1s','4s','mt','ss','me','mo','vo','5s','2s','3s','gm','lm'])
        for card,f_card in tmp:
            if card_code==card:
                return f_card
        print('wrong card input')
    
    def card_switch(self,card_num,click_board):
        if not self.tmp:
            self.tmp = card_num, click_board
            self.highlight_dict[self.color_match['switch']] |= {click_board}
        else:
            pre_card_num, pre_click_board = self.tmp
            self.board_cards[card_num], self.board_cards[pre_card_num] = self.board_cards[pre_card_num], self.board_cards[card_num]
            self.highlight_dict[self.color_match['switch']] |= {click_board}
            self.fade_out[pyxel.frame_count] = {click_board,pre_click_board}
            self.tmp = None

    def card_row_move(self,x,y):
        pass

    def locate_mouse(self,x,y):
        # find if on boards
        print(x,y)
        for locate,location_screen in self.board_map.items():
            screen_x , screen_y = location_screen['x'],location_screen['y']
            if screen_x <= x <= (screen_x +16) and screen_y <= y <= screen_y +16:
                return locate
        # find if on btns

    def board_setting(self):
        result = ['2s'] * 7 + ['1s'] * 5 + ['vo'] * 3 + ['lm'] * 3 + ['ss'] * 3 + ['su'] * 2 + ['mo'] * 2
        # print(result)
        result = [self.card_flip(card) if random.randint(0,1)==1 else card for card in result]
        random.shuffle(result)
        return result

    def location_maping(self):
        """
        2顆星(2 Stars) 3顆星(3 Stars) 7 
        1顆星(1 Star) 4顆星(4 Stars) 5 
        空洞(vo) 5顆星(5 Stars) 3 
        殘月(lm) 盈月(gm) 3 
        流星(ss) 流星體(mt) 3 
        太陽(su) 日蝕(se) 2 
        滿月(mo) 月蝕(me) 2
        """
        self.img_map = dict()
        img_name = ['su','se','4s','1s','ss','mt'
                   ,'mo','me','5s','vo','3s','2s','lm','gm'
                   ,'right','left','up','down'
                   ,'flip','switch','row_move','None']
        img_loc = [{'x':x,'y':y} for y in range(0,16*11,16) for x in range(0,16*2,16)]        
        for name, loc in zip (img_name,img_loc):
            self.img_map[name] = loc
            
        self.board_map = dict()
        for x in range(5):
            for y in range(5):
                self.board_map[(x,y)] = ({'x':25+x*20,'y':30+y*20})
        
        self.board_map['flip']      = {'x':150,'y':30}
        self.board_map['switch']    = {'x':150,'y':50}
        self.board_map['row_move']  = {'x':150,'y':70}

    def highlight_draw(self,board_map_loc,size=20,col=9):
        try:
            location_screen = self.board_map.get(board_map_loc)
            pyxel.rect(location_screen['x']-2,location_screen['y']-2,size,size,col)
        except Exception as e:
            print(f'{e}, {board_map_loc}')

    def board_draw(self,board_map_loc, img_loc,object_size={'wight':16,'height':16},shift_x=0,shift_y=0):
        """
        board_map_loc : tuple or int (int will transfer to  tuple)
        img_loc name of img : str
        object size : default 16 *16
        """
        if type(board_map_loc)==int:
            board_map_loc = (board_map_loc % 5 ,board_map_loc //5,)
        location_screen = self.board_map.get(board_map_loc)
        location_source = self.img_map.get(img_loc)
        if not location_screen and not location_source:
            print(f'{location_screen} or {location_source} not found')
            return
        try:
            pyxel.blt(location_screen['x'] + shift_x, location_screen['y'] + shift_y,0
                     ,location_source['x'], location_source['y']
                     ,object_size['wight'], object_size['height'])
        except Exception as e:
            print(f'error :{e} , {board_map_loc}, {img_loc}')

    def row_move_draw(self):
        down = [self.board_draw((i,0),'down',shift_y=-18) for i in range(5)]
        up = [self.board_draw((i,4),'up'  ,shift_y=18) for i in range(5)]
        left = [self.board_draw((0,i),'right',shift_x=-18) for i in range(5)]
        right = [self.board_draw((4,i),'left',shift_x=18) for i in range(5)]

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
            if self.action == 'flip' and type(click_board) ==tuple:
                card_num = click_board[0] + click_board[1]*5
                self.board_cards[card_num] = self.card_flip(self.board_cards[card_num])

            if self.action == 'switch' and type(click_board) ==tuple:
                card_num = click_board[0] + click_board[1]*5
                self.card_switch(card_num,click_board)
            
            if self.action == 'row_move':
                self.card_row_move(x,y)

            for act_name in ['flip', 'switch','row_move']:
                if click_board == act_name:
                    self.action = act_name if self.action != act_name else None
                self.highlight_dict[self.color_match[act_name]] -= {act_name}

            if self.action:
                self.highlight_dict[self.color_match[self.action]] |= {self.action}

        for start_frame in list(self.fade_out.keys()):
            if pyxel.frame_count - start_frame > self.fade_frame_count:
                    self.highlight_dict[self.color_match['switch']] -= self.fade_out[start_frame]
                    self.fade_out.pop(start_frame)

        # trigger shuffle after sec
        # if self.trigger_shuffle:
        #     if pyxel.frame_count > self.trigger_wait:
        #         self.board_cards = self.board_setting()
        #         self.trigger_shuffle = False

    def draw(self):
        # base background
        pyxel.cls(1)
        pyxel.text(20,5, self.caption, 9)
        pyxel.text(125,5, f'{pyxel.frame_count}', 9)
        pyxel.text(150,7, f'{pyxel.mouse_x,pyxel.mouse_y}', 9)
        
        # effect [highlight]
        if self.highlight_dict:
            for color in self.highlight_dict:
                for loc in self.highlight_dict.get(color):
                    self.highlight_draw(loc,col=color)
        
        # draw main board
        for i in range(25):
            img_name = self.board_cards[i]
            self.board_draw(i,img_name)
        
        if self.action =='row_move':
            self.row_move_draw()

        self.board_draw('flip','flip')
        self.board_draw('switch','switch')
        self.board_draw('row_move','row_move')

if __name__ == '__main__':
    App()