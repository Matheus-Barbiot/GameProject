import bge
import mathutils
from collections import OrderedDict

class Player(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        #PROPRIEDADES PADRÃO:
        self.Character = bge.constraints.getCharacter(self.object)
        self.Scene = bge.logic.getCurrentScene()
        self.Keyboard = bge.logic.keyboard
        self.Mouse = bge.logic.mouse
        
        pass
    def Entradas(self):
        #  Teclado
        self.WKEY = self.Keyboard.inputs[bge.events.WKEY]
        self.SKEY = self.Keyboard.inputs[bge.events.SKEY]
        self.AKEY = self.Keyboard.inputs[bge.events.AKEY]
        self.DKEY = self.Keyboard.inputs[bge.events.DKEY]
        
        self.SPACE = self.Keyboard.inputs[bge.events.SPACEKEY]
        
        
    def update(self):
        self.Entradas()
        
        #### MOVIMENTO:
        y = self.WKEY.active - self.SKEY.active
        x = self.DKEY.active - self.AKEY.active
        
        speed = 0.08
        
        vec = mathutils.Vector([x, y, 0]).normalized() * speed
        self.Character.walkDirection = self.object.worldOrientation * vec
        
        if self.SPACE.activated:
                self.Character.jump()
        pass
