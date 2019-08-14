import random as rm
import matplotlib.pyplot as plt

'''
Created by Ellison William
'''

class Section:
    def __init__(self, id, name, base, size, nearby):
        self.id = id
        self.name = name
        self.base = base
        self.size = size
        self.nearby = nearby

    def is_void(self):
        return self.name.lower() == 'void'


class Memory:
    def __init__(self):
        self.max_limit = 100
        self.ids = []
        self.address_initial = Section(0, "Void", 0, self.max_limit, None)

    def store_firstfit(self, name, size):
        section = self.address_initial

        while section is not None:
            if section.is_void():
                if section.size > size:
                    new_section = Section(0, "Void", section.base + size, section.size - size,
                                          section.nearby)

                    section.id = self.generate_id()
                    section.name = name
                    section.size = size
                    section.nearby = new_section

                    return True

                elif section.size == size:
                    section.id = self.generate_id()
                    section.name = name

                    return True

            section = section.nearby

        print("Não foi possível alocar.")
        return False

    def store_bestfit(self, name, size):
        fragment = 9999
        section = self.address_initial
        section_bestfit = None

        while section is not None:
            if section.is_void():
                frag_local = section.size - size
                if 0 < frag_local < fragment:
                    fragment = frag_local
                    section_bestfit = section

                elif frag_local == 0:
                    section_bestfit = section
                    fragment = 0
                    break

            section = section.nearby

        if section_bestfit:
            if section_bestfit.size > size:
                new_section = Section(0, "Void", section_bestfit.base + size, section_bestfit.size - size,
                                      section_bestfit.nearby)

                section_bestfit.id = self.generate_id()
                section_bestfit.name = name
                section_bestfit.size = size
                section_bestfit.nearby = new_section

                return True

            elif section_bestfit.size == size:
                section_bestfit.id = self.generate_id()
                section.name = name

                return True

        print("Não foi possível alocar.")
        return False

    def store_worstfit(self, name, size):
        fragment = -9999
        section = self.address_initial
        section_worstfit = None

        while section is not None:
            if section.is_void():
                frag_local = section.size - size
                if frag_local > fragment and frag_local >= 0:
                    fragment = frag_local
                    section_worstfit = section

            section = section.nearby

        if section_worstfit:
            if section_worstfit.size > size:
                new_section = Section(0, "Void", section_worstfit.base + size, section_worstfit.size - size,
                                      section_worstfit.nearby)

                section_worstfit.id = self.generate_id()
                section_worstfit.name = name
                section_worstfit.size = size
                section_worstfit.nearby = new_section

                return True

            elif section_worstfit.size == size:
                section_worstfit.id = self.generate_id()
                section.name = name

                return True

        print("Não foi possível alocar.")
        return False

    def remove(self, id):
        if id in self.ids:
            section = self.address_initial

            while section is not None:
                if section.id == id:
                    section.id = 0
                    section.name = "Void"
                    self.ids.remove(id)
                    self.join_empty_memory()

                    return True

                section = section.nearby

        return False

    def compress(self):
        section = self.address_initial

        while section is not None:
            if section.is_void() and (section.nearby is not None):
                copy_size = section.size

                section.id = section.nearby.id
                section.name = section.nearby.name
                section.size = section.nearby.size

                section.nearby.name = 'Void'
                section.nearby.id = 0
                section.nearby.base = section.size + section.base
                section.nearby.size = copy_size

                self.join_empty_memory()

            section = section.nearby

    def join_empty_memory(self):
        section = self.address_initial

        while section is not None:
            if section.is_void() and section.nearby is not None:
                if section.nearby.is_void():
                    section.size += section.nearby.size
                    section.nearby = section.nearby.nearby

                if section.nearby is not None:
                    if section.nearby.is_void():
                        continue

            section = section.nearby
        
        #print("Join feito com sucesso!")

    def generate_id(self):
        id = rm.randint(2000, 2999)

        while id in self.ids:
            id = rm.randint(2000, 2999)
        
        self.ids.append(id)
        return id

    def show_memory(self):
        section = self.address_initial
        print("\nShow Memory:\n{0:4}\t{1:15}\t{2:2}\t{3:2}".format('ID', 'NOME', 'BASE', 'TAMANHO'))
        while section is not None:
            print(f"{section.id:4}\t{section.name:15}\t{section.base}\t{section.size}")
            section = section.nearby

    def show_programs(self):
        programs_name = []
        programs_id = []
        programs_size = []
        section = self.address_initial
        print("\nShow Programs:\n{0:4}\t{1:15}\t{2:2}\t{3:2}".format('ID', 'NOME', 'BASE', 'TAMANHO'))
        while section is not None:
            if not section.is_void():
                print(f"{section.id}\t{section.name:15}\t{section.base}\t{section.size}")
                programs_name.append(section.name)
                programs_id.append(section.id)
                programs_size.append(section.size)

            section = section.nearby

        return programs_name, programs_size, programs_id

    def show_memory_info(self):
        empty_space = 0
        section = self.address_initial
        
        while section is not None:
            empty_space += section.size if section.is_void() else 0
            section = section.nearby

        print(f"Espaço total: {self.max_limit}\nEspaço usado: {self.max_limit - empty_space}\nEspaço vazio: {empty_space}")

        return empty_space, self.max_limit - empty_space


m = Memory()

m.show_memory()
m.store_firstfit("ProcessoA", 16)
m.show_memory()
m.store_firstfit("ProcessoB", 8)
m.show_memory()
m.store_firstfit("ProcessoC", 8)
m.show_memory()
m.store_firstfit("ProcessoD", 2)
m.show_memory()
m.store_firstfit("ProcessoE", 4)
m.show_memory()
m.show_programs()
m.show_memory_info()

while True:
    print("""\n
        ******************************************
        *           SIMULADOR MEMÓRIA            *
        ******************************************
        \t1 - Carregar um programa na memória
        \t2 - Listar programas carregados na memória
        \t3 - Remover um programa da memória
        \t4 - Mostrar espaço total disponível na memória
        \t5 - Mostrar estado atual da memória
        \t6 - Compactar memória
        \t7 - Sair
        *****************************************""")

    option = int(input("Opção: "))

    if option == 1:
        name = input("Digite o nome do programa: ")

        size = 0
        while size not in (2, 4, 8, 16):
            size = int(input("Tamanho (2, 4, 8 ou 16): "))

        while True:
            store_type = int(input("Encaixe: \n(1) Firstfit\n(2) Bestfit\n(3) Worstfit\nDigite o tipo: "))

            if store_type == 1:
                if m.store_firstfit(name, size):
                    print("Adicionado com sucesso!")
                break
            elif store_type == 2:
                if m.store_bestfit(name, size):
                    print("Adicionado com sucesso!")
                break
            elif store_type == 3:
                if m.store_worstfit(name, size):
                    print("Adicionado com sucesso!")
                break
            else:
                print("Digite uma opção válida!")
                continue

    elif option == 2:
        info_programs = m.show_programs()

        labels = []
        sizes = info_programs[1] + [m.max_limit - sum(info_programs[1])]
        for i in range(len(info_programs[0])):
            labels.append(f"{info_programs[2][i]} - {info_programs[0][i]} - {info_programs[1][i]}M")

        labels.append("Espaço vazio")

        figg, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()

    elif option == 3:
        if m.remove(int(input("Digite o id do programa: "))):
            print("Removido com sucesso!")
        else:
            print("Id não existe!")

    elif option == 4:
        info_memory = m.show_memory_info()

        labels = f'Espaço vazio\n{info_memory[0]}M', f'Espaço usado\n{info_memory[1]}M'

        figg, axl = plt.subplots()
        axl.pie(info_memory, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        axl.axis('equal')
        plt.show()

    elif option == 5:
        m.show_memory()

    elif option == 6:
        m.compress()
        print("Compressão realizada com sucesso!")

    elif option == 7:
        break

    else:
        print("Comando inválido, digite novamente!")






