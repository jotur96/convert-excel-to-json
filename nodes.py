from util import Nivel, Parent


class Node:
    
    
    def __init__(self, numero_de_cuenta, descripcion, monto_gs, monto_usd):
        self.numero_de_cuenta = numero_de_cuenta
        self.descripcion = descripcion
        self.monto_gs = monto_gs
        self.monto_usd = monto_usd
        self.children = []
        self.nivel = Nivel.SIN_NIVEL
        
    def add_child(self, child):
        self.children.insert(0, child)
        
    def set_nivel(self, nivel):
        self.nivel = nivel

    def to_dict(self):
        return {
            'numero_de_cuenta': self.numero_de_cuenta,
            'descripcion': self.descripcion,
            'monto_gs': self.monto_gs,
            'monto_usd': self.monto_usd,
            'children': [child.to_dict() for child in self.children],
            'nivel': self.nivel.name  
        }



    

    