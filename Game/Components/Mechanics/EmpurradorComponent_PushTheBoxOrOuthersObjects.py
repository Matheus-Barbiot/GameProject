import bge
from collections import OrderedDict
"""

Componente Empurrador:
    
O componente Empurrador é uma ferramenta útil para criar objetos no Blender Game Engine que respondem a colisões com um objeto específico aplicando força ou movimento. Ele é ideal para criar elementos interativos no jogo, como caixas que andam quando o jogador colide com um sensor.




 ======= Parâmetros =========

ParentName: O nome do objeto que será empurrado quando ocorrer a colisão.
ColisorName: O nome do objeto com o qual o objeto atual deve colidir para ativar o efeito de empurrar.
TypeForce: O tipo de efeito a ser aplicado: "Force" (força) ou "Movement" (movimento).
Axis: A direção do efeito a ser aplicado, representada como um vetor [x, y, z].
Local: Define se a força ou movimento deve ser aplicado em relação às coordenadas locais ou globais.






 ======= Como Usar =========
 
Importar o Componente: Certifique-se de que o script que contém o componente Empurrador esteja acessível no Blender.

Adicionar o Componente: No Blender Game Engine, selecione o objeto ao qual deseja adicionar o componente Empurrador. Acesse o painel "Lógica" nas propriedades do objeto e clique no botão "Add Game Property" para adicionar uma nova propriedade do jogo. Escolha "Python" como o tipo de propriedade e insira Empurrador como o valor da propriedade. Isso associará o componente Empurrador ao objeto.

Configurar os Parâmetros: Na seção "Python Properties" no painel "Lógica", você encontrará os campos para cada parâmetro do componente Empurrador. Preencha esses campos de acordo com suas necessidades.

Preparar os Objetos: Certifique-se de que o objeto de colisão e o objeto pai (que será empurrado) estão devidamente configurados com física ativada e outras configurações necessárias.

Executar o Jogo: Execute o jogo e colida com o objeto de colisão especificado nos parâmetros do componente. O objeto pai deve responder de acordo, aplicando a força ou movimento na direção especificada.




 ========  Exemplos ============
Exemplo de Parâmetros
ParentName: "Caixa"
ColisorName: "Jogador"
TypeForce: "Force"
Axis: [0.0, 0.0, 10.0]
Local: False

Neste exemplo, quando o objeto "Jogador" colidir com o objeto "Caixa", a caixa receberá uma força vertical para cima.

"""
class Empurrador(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ('ParentName', ""), 
    ('ColisorName', ""),
    ('TypeForce', {"Force", "Movement"}),
    ('Axis', [0.0, 0.0, 0.0]),
    ('Local', False)
    ])

    def start(self, args):
        self.Scene = bge.logic.getCurrentScene()
        
        self.objParent = self.Scene.objects[args['ParentName']]
        self.colisor = args['ColisorName']
        self.typeForce = args['TypeForce']
        self.eixo = args['Axis']
        self.local = args['Local']
        
        self.object.collisionCallbacks.append(self.collision)
        pass

    def collision(self, Collisor, collisionPoint, faceNormal):
        if Collisor.name == self.colisor:
            if self.typeForce == 'Movement':
                self.objParent.applyMovement(self.eixo, self.local)
            if self.typeForce == 'Force':
                self.objParent.applyForce(self.eixo, self.local)

    def update(self):
        pass
