import bge
from collections import OrderedDict

class Button(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ('Collisor', ""),
    ('Objeto', ""),
    ('Parâmetro', ""),
    ('DesativarQuandoNaoColidindo', True),
    ])

    def start(self, args):
        self.col = args['Collisor']
        self.obj = args['Objeto']
        self.par = args['Parâmetro']
        
        self.bool = args['DesativarQuandoNaoColidindo']
        self.Scene = bge.logic.getCurrentScene()
        
        self.obj2 = self.Scene.objects[self.obj]
        self.object.collisionCallbacks.append(self.collision)
        pass
    
        
    def collision(self, Collisor, collisionPoint, faceNormal):
        if Collisor.name == self.col:
            self.obj2[self.par] = True
            
    def update(self):
        if self.bool:
            if self.object.collide(self.col)[0] == False:
                self.obj2[self.par] = False
