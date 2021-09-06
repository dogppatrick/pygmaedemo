import pyxel

class App:
    def __init__(self):
        self.width ,self.height = 200, 150
        self.caption = 'When starts are right'
        pyxel.init(self.width,self.height,caption=self.caption)
        pyxel.load("assets/stars_and_btns.pyxres")
        pyxel.mouse(True)
        self.img_mapping()
        self.board_mapping()
        pyxel.run(self.update, self.draw)

    def img_mapping(self):
        self.img_map = []
        for y in range(0,16*10,16):
            for x in range(0,16*2,16):
                self.img_map.append({'x':x,'y':y})
        self.img_map = {i:img for img,i in zip(self.img_map,range(len(self.img_map)))}

    def board_mapping(self):
        self.board_map = dict()
        for x in range(5):
            for y in range(5):
                self.board_map[(x,y)] = ({'x':20+x*25,'y':20+y*25})

    def draw_img(self,board_map_loc, img_loc,object_size={'wight':16,'height':16}):
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
        pyxel.cls(1)
        pyxel.text(20,5, f'When Star Are Right', 9)
        for i in range(5):
            for j in range(5):
                self.draw_img((i,j),(i+j*5)% len(self.img_map))

App()