from APH.Game import *
from APH.Mouse import *
from APH.Utils import *
from APH.Sprite import *

class DragDropSprite(MouseClickSprite):
    def __init__(self):
        MouseClickSprite.__init__(self)
        self.dragging = False
    
    def is_clicked(self, event):
        # If we're dragging, we don't care where the mouse cursor is
        if self.dragging and event.button == 1:
            return True
        if self.rect.collidepoint(event.pos) and event.button == 1:
            return True
        return False
    
    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging = True
            self.drag_offset = (self.position[0] - event.pos[0],
                                self.position[1] - event.pos[1])
            self.real_layer = self.layer
            # Here, we show that we can dynamically add a layer to the top
            # and it not be an issue. It's important not to just use the current
            # top layer, as there may be other sprites in it which get the drop
            # event instead.
            self.old_layers = GetScreen().get_layers()
            layers = GetScreen().get_layers()
            layers.append('DragDropTop')
            GetGame().set_layers(layers)
            self.layer = 'DragDropTop'
            
            # You may find it interesting to implement something such as hiding
            # the mouse cursor while dragging here.
        else:
            self.layer = self.real_layer
            GetGame().set_layers(self.old_layers)
            self.dragging = False
            
    def update(self):
        if self.dragging:
            self.position = (Mouse.get_pos()[0] + self.drag_offset[0],
                             Mouse.get_pos()[1] + self.drag_offset[1])
                             
class DragDropExample(NewGame):
    def transition_in(self):
        self.set_layers(['red', 'blue'])
        red = DragDropSprite()
        red.image = new_surface((50,50))
        red.image.fill((255,0,0))
        red.position = (100, 100)
        red.layer = 'red'
        
        blue = DragDropSprite()
        blue.image = new_surface((75,75))
        blue.image.fill((0,0,255))
        blue.position = (120, 120)
        blue.layer = 'blue'
        
        self.group = MouseGroup(red, blue)


    def main_loop(self):
        self.group.update()
        self.group.draw()
        GetScreen().draw()
        
        # It is important not to pull all the events off the event queue,
        # as you may end up throwing away mouse clicks.
        for event in pygame.event.get(pygame.QUIT):
            self.quit = True

if __name__ == "__main__":
    g = DragDropExample((255, 255, 255), (640, 480), (640, 480), False)
    g.push_state()
    clock = pygame.time.Clock()

    while not GetGame().quit:
        clock.tick(30)
        GetGame().main_loop()