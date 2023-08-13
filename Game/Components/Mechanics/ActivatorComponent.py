import bge
from collections import OrderedDict

class Activator(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ('Object Activator', ""),
    ('Object to Activate', ""),
    ('Property', ""),
    ('Suject to Cancel', True),
    ('Cancel with Distance', True),
    ('Use Key', False),
    ('Distance', 0.000),
    ('Keyboard key', ""),
    ('Input Type', {'Tap', 'Nivel'}),
    ])

    def start(self, args):
        self.scene = bge.logic.getCurrentScene()
        self.keyboard1 = bge.logic.keyboard
        
        self.objActivator = self.scene.objects[args['Object Activator']]
        self.objToActivate = self.scene.objects[args['Object to Activate']]
        self.property = args['Property']
        self.distance = args['Distance']
        self.typeKey = args['Input Type']
        self.Cancel = args['Suject to Cancel']
        self.CancelDistance = args['Cancel with Distance']
        
        self.usekey = args['Use Key']
   
        if self.usekey:
            self.key = args['Keyboard key'].upper()
            self.key2 = f'{self.key}KEY'
            try:
                self.keySuccessfully = eval(f'self.keyboard1.inputs[bge.events.{self.key2}]')
            except:
                print('ERROR! Por favor Digite uma entrada de teclado válida.')
        pass

    def update(self):
        if self.objActivator.getDistanceTo(self.object) < self.distance:
            if self.usekey:
                if self.typeKey == 'Tap':
                    if self.keySuccessfully.activated:
                        if self.Cancel == True:
                            if self.objToActivate[self.property] == True:
                                self.objToActivate[self.property] = False
                            else:
                                self.objToActivate[self.property] = True
                        else:
                            self.objToActivate[self.property] = True
                            
                elif self.typeKey == 'Nivel':
                    if self.keySuccessfully.active:
                        if self.Cancel == True:
                            if self.objToActivate[self.property] == True:
                                self.objToActivate[self.property] = False
                            else:
                                self.objToActivate[self.property] = True
                        else:
                            self.objToActivate[self.property] = True
            else:
                self.objToActivate[self.property] = True
        else:
            if self.CancelDistance == True:
                self.objToActivate[self.property] = False

