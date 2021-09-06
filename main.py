import pyxel
class App:
    def __init__(self):
        self.width ,self.height = 200, 150
        self.caption = 'When starts are right'
        pyxel.init(self.width,self.height,caption=self.caption)
        pyxel.load("assets/stars_and_btns.pyxres")
        pyxel.mouse(True)
        self.location_maping()
        pyxel.run(self.update, self.draw)

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
        
        


    def borad_draw(self,board_map_loc, img_loc,object_size={'wight':16,'height':16}):
        location_screen = self.board_map.get(board_map_loc)
        location_source = self.img_map.get(img_loc)
        if not location_screen and not location_source:
            print(f'{location_screen} or {location_source} not found')
            return
        pyxel.blt(location_screen['x'],location_screen['y'],0,location_source['x'],location_source['y'],object_size['wight'],object_size['height'])
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

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
        img_list = list(self.img_map)
        img_name = img_list[(pyxel.frame_count //50) % len(img_list)]
        print(img_name,pyxel.frame_count)
        self.borad_draw((0,0),img_name)

App()