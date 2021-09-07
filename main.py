import pyxel
import random
class App:
    def __init__(self):
        self.width ,self.height = 200, 150
        self.caption = 'When starts are right'
        pyxel.init(self.width,self.height,caption=self.caption)
        pyxel.load("assets/stars_and_btns.pyxres",True,False,False,False)
        pyxel.mouse(True)
        self.flip_card_status = True
        self.trigger_shuffle = False
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
                   ,'flip','switch']
        img_loc = [{'x':x,'y':y} for y in range(0,16*10,16) for x in range(0,16*2,16)]        
        for name, loc in zip (img_name,img_loc):
            self.img_map[name] = loc
            
        self.board_map = dict()
        for x in range(5):
            for y in range(5):
                self.board_map[(x,y)] = ({'x':20+x*25,'y':20+y*25})
        

    def board_draw(self,board_map_loc, img_loc,object_size={'wight':16,'height':16}):
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
            pyxel.blt(location_screen['x'],location_screen['y'],0,location_source['x'],location_source['y'],object_size['wight'],object_size['height'])
        except Exception as e:
            print(f'error :{e} , {board_map_loc}, {img_loc}')

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            # test shuffle cards
            self.trigger_shuffle = True
            self.trigger_wait = pyxel.frame_count +50        
            
            
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            # test shuffle cards
            # self.board_cards = self.board_setting()
            if self.flip_card_status:
                x = pyxel.mouse_x
                y = pyxel.mouse_y
                click_board = self.locate_mouse(x,y)
                if click_board:
                    card_num = click_board[0] + click_board[1]*5
                    self.board_cards[card_num] = self.card_flip(self.board_cards[card_num])

        if self.trigger_shuffle:
            if pyxel.frame_count > self.trigger_wait:
                self.board_cards = self.board_setting()
                self.trigger_shuffle = False

    def draw(self):
        """
        2顆星(2 Stars) 3顆星(3 Stars) 7 
        1顆星(1 Star) 4顆星(4 Stars) 5 
        空洞(vo) 5顆星(5 Stars) 3 
        殘月(lm) 盈月(gm) 3 
        流星(ss) 流星體(mt) 3 
        太陽(su) 日蝕(se) 2 
        滿月(mo) 月蝕(me) 2
        """
        pyxel.cls(1)
        pyxel.text(20,5, f'When Star Are Right', 9)
        # img_list = list(self.img_map)
        print(pyxel.frame_count)
        for i in range(25):
            img_name = self.board_cards[i]
            self.board_draw(i,img_name)

if __name__ == '__main__':
    App()