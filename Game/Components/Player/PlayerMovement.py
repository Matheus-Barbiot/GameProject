import bge
import mathutils
from collections import OrderedDict

class Player(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ('Speed', 0.000),
    ])

    def start(self, args):
        # PROPRIEDADES PADRÃO:
        self.Character = bge.constraints.getCharacter(self.object)
        self.Scene = bge.logic.getCurrentScene()
        self.Keyboard = bge.logic.keyboard
        self.Mouse = bge.logic.mouse
        
        # ARGUMENTOS MODULARES:
        self.speed = args['Speed']
        
        # VARIAVEIS DE CONFIGURAÇÃO:
        self.roll_x = 0
        self.roll_y = 0
        self.stop_x = False
        self.stop_y = False


        self.climbMode = False
        self.climbCancelar = False
        self.climbSubir = False
        #LOGIC BRICS:
        
        #Sensores:
        self.SENS_Climb = self.object.sensors['Near_Climb']

    ###################################################
    
    def Entradas(self):
        #  Teclado
        self.WKEY = self.Keyboard.inputs[bge.events.WKEY]
        self.SKEY = self.Keyboard.inputs[bge.events.SKEY]
        self.AKEY = self.Keyboard.inputs[bge.events.AKEY]
        self.DKEY = self.Keyboard.inputs[bge.events.DKEY]
        
        self.SPACE = self.Keyboard.inputs[bge.events.SPACEKEY]
        self.SHIFT = self.Keyboard.inputs[bge.events.LEFTSHIFTKEY]
        self.CTRL = self.Keyboard.inputs[bge.events.LEFTCTRLKEY]
    
     ######################################################
     
    def movement(self):
        self.Entradas()
        self.Character.fallSpeed = 55
        #### MOVIMENTO:
        y = self.WKEY.active - self.SKEY.active
        x = self.DKEY.active - self.AKEY.active

        if self.object['Roll Bool']:
            if not self.stop_x:
                # Armazena a direção do movimento enquanto rolando
                self.roll_x = self.DKEY.active - self.AKEY.active
                if self.roll_x != 0:
                    self.stop_x = True
            if not self.stop_y:
                self.roll_y = self.WKEY.active - self.SKEY.active
                if self.roll_y != 0:
                    self.stop_y = True
            
            speed2 = self.speed * 1.5
            
            vec = mathutils.Vector([self.roll_x, self.roll_y, 0]).normalized() * speed2
            self.Character.walkDirection = self.object.worldOrientation * vec
            
        else:
            # Reinicia as variáveis de controle quando não estiver rolando
            self.stop_x = False
            self.stop_y = False
            
            # Usa a direção do movimento normal se não estiver rolando
            vec = mathutils.Vector([x, y, 0]).normalized() * self.speed
            self.Character.walkDirection = self.object.worldOrientation * vec
        
        if self.SPACE.activated:
            if self.SENS_Climb.positive:
                self.climbMode = True
                return
            else:
                self.Character.jump()
        if self.SHIFT.activated:
            self.object['Roll Bool'] = True
            
        #############################################################
        
    def climb(self):
        self.Entradas()
        self.Character.fallSpeed = 0
        if self.climbSubir == False:
            if self.SENS_Climb.hitObject != None:
                objetoColidido = self.SENS_Climb.hitObject

                
                self.object.localPosition.z = objetoColidido.worldPosition.z
                self.object.localPosition.y = objetoColidido.localPosition.y
                self.object.localOrientation = objetoColidido.localOrientation
            
                vec = mathutils.Vector([(self.DKEY.active - self.AKEY.active), 0, 0]).normalized() * self.speed
                self.Character.walkDirection = self.object.worldOrientation * vec
                
                if self.SPACE.activated:
                    target = self.Scene.objects['target']
                    origin = self.Scene.objects['origin']
                    hit, pos, normal = self.object.rayCast(target, origin, 0.0, "Ground", 1,1,0)

                    if hit:
                        self.climbSubir = True
                        
                        ob = self.Scene.addObject('Esfera UV', self.object)
                        ob.worldPosition = pos + mathutils.Vector([0, 0, 1])

                if self.CTRL.activated:
                    self.climbCancelar = True
                    self.climbMode = False
            else:
                self.climbCancelar = True
                self.climbMode = False
        else:
            if not 'Esfera UV' in self.Scene.objects:
                self.climbSubir = False
                self.climbMode = False
                return
            else:
                target_position = self.Scene.objects['Esfera UV'].worldPosition
                direction = target_position - self.object.worldPosition
                normalized_direction = direction.normalized()

            # Define a velocidade para a direção calculada
            vec = normalized_direction * 0.08

            # Define a walkDirection para a direção calculada
            self.Character.walkDirection = vec
            
            

                
        ###############################################################
    def update(self):
        if self.climbMode == True:
            self.climb()
        else:
            self.movement()



