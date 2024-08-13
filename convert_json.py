from asyncio import sleep
import pandas as pd
import json

from nodes import Node, Parent, Nivel

# Cargar los datos

# Crear nodos para cada fila en el DataFrame
class ConvertToJson:
    

    nodes = []

    def create_nodes(self, file_path):


        df = pd.read_excel(file_path, sheet_name='Database')
        
        for index, row in df[::-1].iterrows():
            numero_de_cuenta = str(row['NUMERO_DE_CUENTA'])
            descripcion = row['CUENTA']
            monto_gs = row['MONTO_GS']
            monto_usd = row['MONTO_USD']
            
            # Crear un nodo con la descripción y los montos
            if monto_gs == 0:
                continue
            
            node = Node(numero_de_cuenta, descripcion, monto_gs, monto_usd)
            
            # Almacenar el nodo en el diccionario
            self.nodes.append(node)
            


    def link_nodes(self):
        # Convertir el árbol a una estructura de diccionarios
        nodes = self.nodes
        children_n1 = []
        children_n2 = []
        children_n3 = []
        parents = []
        parent = 0
        sum_monto_gs = 0
        is_parent = Parent.NONE
        nivel = Nivel.UNO
        
        # print(len(nodes[-1].children))
        count = 0
        while (len(nodes) != 0):
            count += 1
            # print("while count: ", count)
            for i in range(len(nodes)):
                # print("for i: ", i)
                # print(nodes[i].__dict__)
                # print("sum_monto_gs: ", sum_monto_gs)
                
                sum_monto_gs_n1 =  sum(x.monto_gs for x in children_n1)
                sum_monto_gs_n2 =  sum(x.monto_gs for x in children_n2)
                sum_monto_gs_n3 =  sum(x.monto_gs for x in children_n3)
                sum_monto_usd_n1 =  sum(x.monto_usd for x in children_n1)
                sum_monto_usd_n2 =  sum(x.monto_usd for x in children_n2)
                sum_monto_usd_n3 =  sum(x.monto_usd for x in children_n3)
                
                # if is_parent == Parent.IS_PARENT:
                #     print("IS PARENT?")
                #     sum_parents = 0
                #     try:
                #         print(nodes[i].__dict__)
                #         print(nodes[i+1].__dict__)
                #         if nodes[i].monto_gs != nodes[i+1].monto_gs:
                #             print("NO IS PARENT")
                #             is_parent = Parent.NONE
                #             nivel = Nivel.UNO
                #             continue
                #         else:
                #             print("IS PARENT")
                #             is_parent = Parent.IS_PARENT
                #             parent = i
                #             nivel = nivel + 1
                #     except Exception as e:
                #         print (e)
                        # is_parent = Parent.NONE                
                
                if nodes[i].monto_gs == sum_monto_gs_n1 or nodes[i].monto_usd == sum_monto_usd_n1:
                    # print(i)
                    is_parent = Parent.MAYBE
                    try:
                        is_parent = Parent.IS_PARENT
                        parent = i
                        nivel = Nivel.DOS
                            
                    except Exception as e:
                        # print (e)
                        is_parent = Parent.NONE
                        
                if nodes[i].monto_gs == sum_monto_gs_n2 or nodes[i].monto_usd == sum_monto_usd_n2:
                    # print(i)
                    is_parent = Parent.MAYBE
                    try:
                        is_parent = Parent.IS_PARENT
                        parent = i
                        nivel = Nivel.TRES
                            
                    except Exception as e:
                        # print (e)
                        is_parent = Parent.NONE
                        
                if nodes[i].monto_gs == sum_monto_gs_n3 or nodes[i].monto_usd == sum_monto_usd_n3:
                    # print(i)
                    is_parent = Parent.MAYBE
                    try:
                        is_parent = Parent.IS_PARENT
                        parent = i
                        nivel = Nivel.CUATRO
                            
                    except Exception as e:
                        # print (e)
                        is_parent = Parent.NONE
                        
                if is_parent == Parent.IS_PARENT:
                    # print(i)
                    # print("is parent: ")
                    # print("nivel: ", nivel)
                    if nivel == Nivel.DOS:
                        # print("nivel dos")
                        nodes[parent].set_nivel(Nivel.DOS)
                        for children in children_n1:
                            nodes[parent].add_child(children)
                        children_n2.append(nodes[parent])
                        children_n1.clear()
                        
                    if nivel == Nivel.TRES:
                        # print("nivel tres")
                        nodes[parent].set_nivel(Nivel.TRES)
                        for children in children_n2:
                            nodes[parent].add_child(children)
                        children_n3.append(nodes[parent])
                        children_n2.clear()
                        
                    if nivel == Nivel.CUATRO:
                        # print("nivel parent")
                        nodes[parent].set_nivel(Nivel.CUATRO)
                        for children in children_n3:
                            nodes[parent].add_child(children)
                        parents.append(nodes[parent])
                        children_n3.clear()
                    
                    for j in range(len(nodes)):
                        if j <= i:
                            # print("eliminar: ", j)
                            # print(nodes[0].__dict__)
                            nodes.pop(0)                    

                    is_parent = Parent.NONE
                    nivel = Nivel.UNO
                    break
                

                
                if nivel == Nivel.UNO:
                    nodes[i].set_nivel(Nivel.UNO)
                    children_n1.append(nodes[i])
                    # print("Add nivel uno")
                    
                # print("monto_gs nodo: ", nodes[i].monto_gs)
                # print("sum_monto_gs_n1: ", sum_monto_gs_n1)
                # print("sum_monto_gs_n2: ", sum_monto_gs_n2)
                # print("sum_monto_gs_n3: ", sum_monto_gs_n3)
                # sum_monto_gs += nodes[i].monto_gs
            #     if i == 10:
            #         break
            # if count == 10:
            #     break
        return parents
    
    
    
    def to_dict(self, parents):
        data = []
        for parent in parents:
            node_data = parent.to_dict()
            data.insert(0, node_data)

        return data



    def convert(self, file_path):
        self.create_nodes(file_path)
        
        parents = self.link_nodes()

        data = self.to_dict(parents)
        
        with open('./file/output.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            
        # print(data)
        
        return data
        
        
        # print_notes()

    