import bge
import mathutils
from collections import OrderedDict

class Player(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ('Movemento', 0.000),
    ('Rolagem', 0.000),
    ('Gravity', 0.000),
    
    ('Climb - ObjetoCaminho', ""),
    ('Climb - Vel Inicio', 0.000),
    ('Climb - Vel Movimento', 0.000),
    ('Climb - Vel Subida', 0.000),
    ])

    def start(self, args):
        # PROPRIEDADES PADRÃO:
        self.Character = bge.constraints.getCharacter(self.object)
        self.Scene = bge.logic.getCurrentScene()
        self.Keyboard = bge.logic.keyboard
        self.Mouse = bge.logic.mouse
        
        # ARGUMENTOS MODULARES:
        self.speed = args['Movemento']
        self.rollSpeed = args['Rolagem']
        self.fallSpeed = args['Gravity']
        
        self.climbObject = args['Climb - ObjetoCaminho']
        self.climbInicial = args['Climb - Vel Inicio']
        self.climbMovement = args['Climb - Vel Movimento']
        self.climbSubida = args['Climb - Vel Subida']
        
        # VARIAVEIS DE CONFIGURAÇÃO:
        self.roll_x = 0
        self.roll_y = 0
        self.stop_x = False
        self.stop_y = False


        self.climbMode = False
        self.climbAtivar = False
        self.climbCancelar = False
        self.climbSubir = False
        #LOGIC BRICS:
        
        #Sensores:
        self.SENS_Climb = self.object.sensors['Near_Climb']
        self.SENS_Climb2 = self.object.sensors['Collision']

#############################################################################################################      
#############################################################################################################
    
    def Entradas(self):
        #  Teclado
        self.WKEY = self.Keyboard.inputs[bge.events.WKEY]
        self.SKEY = self.Keyboard.inputs[bge.events.SKEY]
        self.AKEY = self.Keyboard.inputs[bge.events.AKEY]
        self.DKEY = self.Keyboard.inputs[bge.events.DKEY]
        
        self.SPACE = self.Keyboard.inputs[bge.events.SPACEKEY]
        self.SHIFT = self.Keyboard.inputs[bge.events.LEFTSHIFTKEY]
        self.CTRL = self.Keyboard.inputs[bge.events.LEFTCTRLKEY]
    
#############################################################################################################      
#############################################################################################################
     
    def movement(self):
        if self.Character.onGround:
            self.climbCancelar = False
        # DADOS NECESSÁRIOS:
        self.Character.fallSpeed = self.fallSpeed
        self.Entradas()
        
        y = self.WKEY.active - self.SKEY.active
        x = self.DKEY.active - self.AKEY.active

        
        # ROLAR:
        if self.object['Roll Bool']:
            if self.object.scaling.z != 0.5:
                self.object.scaling.z = 0.5
            if not self.stop_x:
                self.roll_x = self.DKEY.active - self.AKEY.active
                if self.roll_x != 0:
                    self.stop_x = True
            
            if not self.stop_y:
                self.roll_y = self.WKEY.active - self.SKEY.active
                if self.roll_y != 0:
                    self.stop_y = True
            
            vec = mathutils.Vector([self.roll_x, self.roll_y, 0]).normalized() * self.rollSpeed
            self.Character.walkDirection = self.object.worldOrientation * vec
        
   
        # MOVEMENTOS:
        else:
            
            self.stop_x = False
            self.stop_y = False
            
            vec = mathutils.Vector([x, y, 0]).normalized() * self.speed
            self.Character.walkDirection = self.object.worldOrientation * vec
        
   
        # AJUSTAR ROTAÇÃO:
        teclasList = [self.WKEY, self.SKEY, self.AKEY, self.DKEY]
        lc1 = self.Scene.objects['CameraAngX'].localOrientation[1][0:2]
        lc2 = self.Scene.objects['CameraAngX'].localOrientation[0][0:2]
        
        self.object.localOrientation[1][0:2]
        self.object.localOrientation[0][0:2]
                
        for tecla in teclasList:
            if tecla.active:
                self.object.localOrientation[1][0:2] = lc1
                self.object.localOrientation[0][0:2] = lc2
                if self.SENS_Climb.positive and self.Character.onGround == False:
                    if self.climbCancelar == False:
                        self.climbMode = True
                        return
                
        
        if self.WKEY.active or self.SKEY.active or self.AKEY.active or self.DKEY.active:
            self.Character.fallSpeed = self.fallSpeed
        
        elif self.Character.onGround == False:
            self.Character.fallSpeed = self.fallSpeed
        else:
            self.Character.fallSpeed = 0
        
                         
                
        # PULO \ ATIVAR CLIMB
        if self.climbCancelar == False:
            if self.SPACE.activated:
                if self.SENS_Climb.positive:
                    self.climbMode = True
                    return
                else:
                    self.Character.jump()
                
        if self.climbCancelar == False:
            if self.SPACE.active:
                if self.SENS_Climb.positive:
                    self.climbMode = True
                    return
            
                
        # ATIVAR ROLAGEM:
        if self.SHIFT.activated:
            self.object['Roll Bool'] = True
            
#############################################################################################################      
#############################################################################################################
        
    def climb(self):
        # DADOS NECESSÁRIOS:
        self.Entradas()
        self.Character.fallSpeed = 0
        
        # PERSONAGEM SE PENDURA - INÍCIO DE CLIMB:
        if self.SENS_Climb.hitObject != None:
            if self.SENS_Climb2.positive:
                if self.object.worldPosition.z != self.SENS_Climb.hitObject.worldPosition.z:
                    self.object.applyMovement([0, 0.25, self.climbInicial], True)
                    
            else: 
                if self.climbSubir == False: ######## CLIMB ATIVO:
                    
                # movimento com A e D - MOVIMENTO LATERAL:
                    self.object.worldOrientation = self.SENS_Climb.hitObject.worldOrientation
                    
                    vec = mathutils.Vector([(self.DKEY.active - self.AKEY.active),0, 0]).normalized() * self.climbMovement
                    self.Character.walkDirection = self.object.worldOrientation * vec
                    
                    self.object.applyMovement([0, 0.05, 0], True)
                    
                    
                # PERSONAGEM SOBE A ESTRUTURA QUE ESTÁ PENDURADO:
                    if self.SPACE.activated:
                        target = self.Scene.objects['target']
                        origin = self.Scene.objects['origin']
                        hit, pos, normal = self.object.rayCast(target, origin, 0.0, "Ground", 1,1,0)

                        if hit:
                            self.climbSubir = True
                            ob = self.Scene.addObject(self.climbObject, self.object)
                            ob.worldPosition = pos + mathutils.Vector([0, 0, 1])
                    
                # CANCELA O CLIMB
                    if self.CTRL.activated:
                        self.climbMode = False
                        self.climbCancelar = True
                    
                    print(self.climbCancelar)
                    if self.climbCancelar == True:
                        self.Character.fallSpeed = self.fallSpeed
                        self.climbMode = False
                        return
                # AJUSTES PARA A ESCALADA:
                else:
                    if not self.climbObject in self.Scene.objects:
                        self.climbSubir = False
                        self.climbMode = False
                        return
                    else:
                        target_position = self.Scene.objects[self.climbObject].worldPosition
                        direction = target_position - self.object.worldPosition
                        normalized_direction = direction.normalized()

                        vec = normalized_direction * self.climbSubida
                        self.Character.walkDirection = vec  
        else:
            self.climbSubir = False
            self.climbMode = False



                
#############################################################################################################      
#############################################################################################################

    def update(self):
        if self.climbMode == True:
            if self.climbCancelar == False:
                self.climb()
            else:
                self.movement()
        else:
            self.movement()
        
        