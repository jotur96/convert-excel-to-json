from asyncio import sleep
import pandas as pd
import json
import math

from nodes import Node, Parent, Nivel

# Cargar los datos

# Crear nodos para cada fila en el DataFrame
class ConvertToJson:
    

    nodes = []
        
    def create_nodes(self, file_path, inverse):
        df = pd.read_excel(file_path, sheet_name=0)
        
        if inverse:        
            df = df[::-1].iterrows()
        else:
            df = df.iterrows()
        
        for index, row in df:
            numero_de_cuenta = str(row['NUMERO_DE_CUENTA']) if 'NUMERO_DE_CUENTA' in row else None
            descripcion = row['CUENTA'] if 'CUENTA' in row else None
            monto_gs = row['MONTO_GS'] if 'MONTO_GS' in row else None
            monto_usd = row['MONTO_USD'] if 'MONTO_USD' in row else None
            
            # Crear un nodo con la descripción y los montos
            if monto_gs == 0 or monto_gs is None or (isinstance(monto_gs, float) and math.isnan(monto_gs)):
                continue
            
            node = Node(numero_de_cuenta, descripcion, monto_gs, monto_usd)
            
            # Almacenar el nodo en el diccionario
            self.nodes.append(node)
            
   
    def link_nodes(self):
        result = {}  # Usaremos un diccionario para almacenar los niveles
        nivel_mayor = 0

        while len(self.nodes) > 0:
            node = self.nodes.pop()
            self.log("nodo actual: ", node.__dict__)
            
            if 0 not in result:
                # Si el nivel 0 no existe, lo creamos y agregamos el nodo
                result[0] = [node]
                node.set_nivel(0)
                continue

            for index in sorted(result.keys()):
                nivel = result[index]
                # self.log(f"Nivel {index}: ", [nodo.numero_de_cuenta for nodo in nivel])

                sum_monto_gs = sum(data.monto_gs if data.monto_gs is not None else 0 for data in nivel)
                sum_monto_usd = sum(data.monto_usd if data.monto_usd is not None else 0 for data in nivel)

                # self.log("sum_monto_gs: ", sum_monto_gs)
                # self.log("sum_monto_usd: ", sum_monto_usd)

                if node.monto_gs == sum_monto_gs or node.monto_usd == sum_monto_usd:
                    
                    for data in nivel:
                        node.add_child(data)
                    
                    nuevo_nivel = index + 1
                    
                    result[index].clear()
                    node.set_nivel(nuevo_nivel)
                    self.log("nuevo nivel: ", nuevo_nivel)
                    
                    if nuevo_nivel > nivel_mayor:
                        nivel_mayor = nuevo_nivel                  

                    if (nuevo_nivel) in result:
                        # result[nuevo_nivel].append(node)
                        result[nuevo_nivel].insert(0, node)
                    else:
                        result[nuevo_nivel] = [node]     
                    break

                if index == max(result.keys()):
                    # result[0].append(node)
                    result[0].insert(0, node)

        self.log("result: ", result)
        # self.log("result: ", result[nivel_mayor])
        return result
    
    
    
        
    
    def to_dict(self, result):
        data = []
        self.log("parents: ", result)
        
        for index in sorted(result.keys()):
            nodes = result[index]
            for node in nodes:
                node_data = node.to_dict()
                data.append(node_data)

        return data


    def convert(self, file_path):
        self.create_nodes(file_path, False)
        
        result = self.link_nodes()
        
        total_elements = sum(len(nodes) for nodes in result.values())
        self.log("total_elements: ", total_elements)
        
        
        if total_elements == 0:
            self.create_nodes(file_path, True)
            result = self.link_nodes()
        
        total_elements = sum(len(nodes) for nodes in result.values())
        self.log("total_elements: ", total_elements)

        data = self.to_dict(result)
        
        with open('./file/output.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            
        # self.log(data)
        
        return data
        
        
    def log(self, *args):
        # print(*args)
        pass



    