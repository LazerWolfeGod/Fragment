from Camera import Camera

class Player:
    def __init__(self,x,y,camera):
        self.x = x
        self.y = y
        self.has_camera = camera
        if self.has_camera:
            self.camera = Camera(self)
    def render(self):
        pass
        
        
        
