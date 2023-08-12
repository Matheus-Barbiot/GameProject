import bge
from mathutils import Vector
from collections import OrderedDict

class CameraAng(bge.types.KX_PythonComponent):
    args = OrderedDict([])

    def start(self, args):
        self.Mouse_ = bge.logic.mouse
        pass

    def update(self):
        if self.Mouse_.inputs[bge.events.WHEELUPMOUSE].active:
            if self.object.worldScale > Vector((1, 1, 1)):
                self.object.worldScale -= Vector((0.1, 0.1, 0.1))

        elif self.Mouse_.inputs[bge.events.WHEELDOWNMOUSE].active:
            if self.object.worldScale < Vector((3, 3, 3)):
                self.object.worldScale += Vector((0.1, 0.1, 0.1))
        pass
