import random as rm
import matplotlib.pyplot as plt

"""
Desenvolvido por:
Ellison William Medrado Guimarães
Matheus Santos Rodrigues
Saionara Aguiar Gomes
"""


class Section:
    """
    Essa classe é responsável por representar cada bloco na memória
    """
    def __init__(self, id, name, base, size, nearby):
        self.id = id
        self.name = name
        self.base = base
        self.size = size
        self.nearby = nearby

    def is_void(self):
        """Return: Se o objeto for um espaço vazio (True), senão (False)."""
        return self.name.lower() == 'void'


class Memory:
    """
    Classe responsável por gerênciar a memória.
        - Inserir via firstfit, nextfit, bestfit e worstfit;
        - Remover por Id;
        - Mostrar processos inseridos na memória;
        - Mostrar o estado atual da memória (espaços em branco e preenchidos);
        - Mostrar espaço usado, vazio e total da memória.
    """
    def __init__(self):
        """
        Inicializando os dados da memória.
            - Tamanho máximo da memória (max_limit = 100)
            - Lista com Ids dos processos existente na memória
            - Endereço ou "ponteiro" do primeiro bloco da lista encadeada
            - Endereço do último bloco adicionado a memória (last_acess)
        """
        self.max_limit = 100
        self.ids = []
        self.address_initial = Section(0, "Void", 0, self.max_limit, None)
        self.last_acess = self.address_initial

    def store_firstfit(self, name, size):
        """
        Insere na memória através do método firstfit.
        :return: Retorna True se for inserido com sucesso e False se não for.
        """
        # Cópia do endereço inicial para percorrer a lista encadeada
        section = self.address_initial

        # Enquanto section NÃO for None
        while section is not None:
            # Verifica se é um bloco vazio
            if section.is_void():
                # Se for vazio, verifica se é maior ou igual ao tamanho informado.
                if section.size > size:
                    # Se for maior, é criado uma nova section com o fragmento
                    new_section = Section(0, "Void", section.base + size, section.size - size,
                                          section.nearby)
                    # Muda as informações da section para as atuais
                    section.id = self.generate_id()
                    section.name = name
                    section.size = size
                    # Aponta o ponteiro pro próximo para o fragmento vazio
                    section.nearby = new_section
                    # Atualiza o ponteiro do ultimo endereço adicionado (last_acess)
                    self.last_acess = section

                    return True

                elif section.size == size:
                    # Se for igual, somente é necessário substituir os dados
                    section.id = self.generate_id()
                    section.name = name
                    # Atualiza o ponteiro do ultimo endereço adicionado (last_acess)
                    self.last_acess = section

                    return True

            # Aponta para o próximo endereço para continuar a percorrer
            section = section.nearby

        print("Não foi possível alocar.")
        return False

    def store_nextfit(self, name, size):
        """
        Insere na memória através do método nextfit.

        A diferença na implementação desse método é que começa a percorrer
        do ultimo endereço adicionado a memória. Com isso, não percorre
        inicialmente de address_initial e sim de last_acess.
        Consequentemente, ao chegar no final e não encotrar, é necessário
        voltar o ponteiro pro início e percorrer até encontrar last_acess.

        Diferença na implementação:
            - section começa de last_acess.nearby e não de address_initial
            - Percorrer enquanto section != self.last_acess, e não enquanto
            section is not None.
            - E no final do laço, perguntar se está no final da lista encadeada
            para retornar o ponteiro ao início.

        :return: Retorna True se for inserido com sucesso e False se não for.
        """
        # Cópia do endereço após o last_acess para percorrer a lista encadeada a partir
        # do ultimo inserido.
        section = self.last_acess.nearby

        ''' Enquanto o endereço de section for diferente do endereço do bloco do ultimo acesso,
            é porque não percorreu do last_acess até o final e do início até o last_acess.
            Isso é feito para percorrer até o final, e do final, caso não ache, volte para o 
            início da lista encadeada e percorre até achar a last_acess para encontrar espaço vazio.'''
        while section != self.last_acess:
            if section.is_void():
                if section.size > size:
                    new_section = Section(0, "Void", section.base + size, section.size - size,
                                          section.nearby)

                    section.id = self.generate_id()
                    section.name = name
                    section.size = size
                    section.nearby = new_section
                    self.last_acess = section

                    return True

                elif section.size == size:
                    section.id = self.generate_id()
                    section.name = name
                    self.last_acess = section

                    return True

            section = section.nearby

            # Se chegar ao final da lista e não encontrar espaço, retorna
            # o ponto section para o início da lista encadeada.
            if section is None:
                section = self.address_initial

        print("Não foi possível alocar.")
        return False

    def store_bestfit(self, name, size):
        """
        Insere na memória através do método bestfit.
        :return: Retorna True se for inserido com sucesso e False se não for.
        """
        # Inicia o tamanho do fragmento com um número grande
        fragment = 9999
        # Cópia do endereço inicial para percorrer a lista encadeada
        section = self.address_initial
        # Endereço do melhor bloco para inserir
        section_bestfit = None

        '''Nesse laço, pesquisamos qual o melhor bloco a ser inserido.
        No final do laço, section_bestfit terá o endereço do melhor local.
        Se não houver espaço, section_bestfit continuará sendo None'''
        # Enquanto section NÃO for None
        while section is not None:
            # Verifica se é um bloco vazio
            if section.is_void():
                # Se for vazio:
                # Calcula o fragmento local com base no tamanho do espaço vazio e do espaço necessário
                frag_local = section.size - size
                # Se o fragmento estiver entre 0 e o fragment mínimo.
                if 0 < frag_local < fragment:
                    # fragment recebe o fragmento calculado
                    fragment = frag_local
                    # encontramos uma section possível e armazenamos o endereço
                    section_bestfit = section

                # Se o fragmento local for igual a 0, está no lugar ideal para colocar o processo.
                elif frag_local == 0:
                    # encontramos uma section IDEAL e armazenamos o endereço
                    section_bestfit = section
                    fragment = 0
                    break

            # Aponta para o próximo endereço para continuar a percorrer
            section = section.nearby

        # Verifica se section_bestfit não é None
        if section_bestfit:
            # Se não for None, verifica qual é o tamanho
            if section_bestfit.size > size:
                # Se for maior, é criado uma nova section com o fragmento
                new_section = Section(0, "Void", section_bestfit.base + size, section_bestfit.size - size,
                                      section_bestfit.nearby)
                # Muda as informações da section para as atuais
                section_bestfit.id = self.generate_id()
                section_bestfit.name = name
                section_bestfit.size = size
                # Aponta o ponteiro pro próximo para o fragmento vazio
                section_bestfit.nearby = new_section
                # Atualiza o ponteiro do ultimo endereço adicionado (last_acess)
                self.last_acess = section_bestfit

                return True

            elif section_bestfit.size == size:
                # Se for igual, somente é necessário substituir os dados
                section_bestfit.id = self.generate_id()
                section.name = name
                # Atualiza o ponteiro do ultimo endereço adicionado (last_acess)
                self.last_acess = section_bestfit

                return True

        print("Não foi possível alocar.")
        return False

    def store_worstfit(self, name, size):
        # Inicia o tamanho do fragmento com um número muito pequeno
        fragment = -9999
        # Cópia do endereço inicial para percorrer a lista encadeada
        section = self.address_initial
        # Endereço do PIOR bloco para inserir
        section_worstfit = None

        '''Nesse laço, pesquisamos qual o PIOR bloco a ser inserido.
        No final do laço, section_worstfit terá o endereço do pior local.
        Se não houver espaço, section_worstfit continuará sendo None'''
        # Enquanto section NÃO for None
        while section is not None:
            # Verifica se é um bloco vazio
            if section.is_void():
                # Se for vazio:
                # Calcula o fragmento local com base no tamanho do espaço vazio e do espaço necessário
                frag_local = section.size - size
                # Se o fragmento local for maior que o fragmento anterior e fragmento local for positivo
                if frag_local > fragment and frag_local >= 0:
                    # fragment recebe o fragmento calculado
                    fragment = frag_local
                    # encontramos uma section possível e armazenamos o endereço
                    section_worstfit = section

            # Aponta para o próximo endereço para continuar a percorrer
            section = section.nearby

        # Verifica se section_worstfit não é None
        if section_worstfit:
            # Se não for None, verifica qual é o tamanho
            if section_worstfit.size > size:
                # Se for maior, é criado uma nova section com o fragmento
                new_section = Section(0, "Void", section_worstfit.base + size, section_worstfit.size - size,
                                      section_worstfit.nearby)
                # Muda as informações da section para as atuais
                section_worstfit.id = self.generate_id()
                section_worstfit.name = name
                section_worstfit.size = size
                # Aponta o ponteiro pro próximo para o fragmento vazio
                section_worstfit.nearby = new_section
                # Atualiza o ponteiro do ultimo endereço adicionado (last_acess)
                self.last_acess = section_worstfit

                return True

            elif section_worstfit.size == size:
                # Se for igual, somente é necessário substituir os dados
                section_worstfit.id = self.generate_id()
                section.name = name
                # Atualiza o ponteiro do ultimo endereço adicionado (last_acess)
                self.last_acess = section_worstfit

                return True

        print("Não foi possível alocar.")
        return False

    def remove(self, id):
        """
        Remove um bloco da memória através do id.
        :return: Retorna True se for removido com sucesso e False se não for.
        """
        # Se o id estiver na lista de ids
        if id in self.ids:
            # Cópia do endereço inicial para percorrer a lista encadeada
            section = self.address_initial

            # Enquanto section NÃO for None
            while section is not None:
                # Verifica se o Id da section é igual ao Id informado
                if section.id == id:
                    # Se sim, zera o bloco
                    section.id = 0
                    section.name = "Void"
                    # Remove da lista de Id
                    self.ids.remove(id)
                    # Une espaços em brancos que estão juntos
                    self.join_empty_memory()

                    return True

                # Aponta para o próximo endereço para continuar a percorrer
                section = section.nearby

        return False

    def compress(self):
        """
        Reorganiza os processos de modo que não fique qualquer espaço livre entre
        os processos.
        """
        # Cópia do endereço inicial para percorrer a lista encadeada
        section = self.address_initial

        # Enquanto section NÃO for None
        while section is not None:
            # Verifica se a sessão é vazia e se o próximo não é None
            if section.is_void() and (section.nearby is not None):
                # Se a condição for satisfeita:

                copy_size = section.size
                # Configura o bloco vazio com o processo seguinte
                section.id = section.nearby.id
                section.name = section.nearby.name
                section.size = section.nearby.size
                # Configura o processo seguinte como um espaço vazio
                section.nearby.name = 'Void'
                section.nearby.id = 0
                section.nearby.base = section.size + section.base
                section.nearby.size = copy_size
                # Une blocos vazios que estão juntos
                self.join_empty_memory()

            # Aponta para o próximo endereço para continuar a percorrer
            section = section.nearby

    def join_empty_memory(self):
        """
        Une os blocos em brancos que estão juntos
        """
        # Cópia do endereço inicial para percorrer a lista encadeada
        section = self.address_initial

        # Enquanto section NÃO for None
        while section is not None:
            # Se o bloco for vazio e o próximo não for None
            if section.is_void() and section.nearby is not None:
                # Verifica se o próximo bloco é vazio também
                if section.nearby.is_void():
                    # Se for vazio, une os blocos
                    section.size += section.nearby.size
                    section.nearby = section.nearby.nearby

                # Se o próximo bloco além dos dois ainda for branco, o laço repete
                # passando o mesmo section
                if section.nearby is not None:
                    if section.nearby.is_void():
                        continue

            # Aponta para o próximo endereço para continuar a percorrer
            section = section.nearby

    def generate_id(self):
        """
        Gera um novo id aleatório entre 2000 e 2999 não repetido
        :return: Id not repeated
        """
        id = rm.randint(2000, 2999)

        while id in self.ids:
            id = rm.randint(2000, 2999)
        
        self.ids.append(id)
        return id

    def show_memory(self):
        """
        Mostra na tela a situação atual da memória, espaços ocupados por processos e espaços
        vazios
        """
        section = self.address_initial
        print("\nShow Memory:\n{0:4}\t{1:15}\t{2:2}\t{3:2}".format('ID', 'NOME', 'BASE', 'TAMANHO'))
        while section is not None:
            print(f"{section.id:4}\t{section.name:15}\t{section.base}\t{section.size}")
            section = section.nearby

    def show_programs(self):
        """
        Mostra na tela todos os programas carregados na memória até o momento.
        :return: Três listas. A primeira contém o nome dos programas, a segunda
        o tamanho e na terceira o id dos programas.
        """
        # Aloca as 3 listas
        programs_name = []
        programs_id = []
        programs_size = []

        # Cópia do endereço inicial para percorrer a lista encadeada
        section = self.address_initial

        print("\nShow Programs:\n{0:4}\t{1:15}\t{2:2}\t{3:2}".format('ID', 'NOME', 'BASE', 'TAMANHO'))

        # Enquanto section NÃO for None
        while section is not None:
            # Se o espaço não for vazio
            if not section.is_void():
                # Imprime e adiciona a lista
                print(f"{section.id}\t{section.name:15}\t{section.base}\t{section.size}")
                programs_name.append(section.name)
                programs_id.append(section.id)
                programs_size.append(section.size)

            # Aponta para o próximo endereço para continuar a percorrer
            section = section.nearby

        return programs_name, programs_size, programs_id

    def show_memory_info(self):
        """
        Mostra na tela o espaço total, o espaço usado e o espaço vazio.
        :return: espaço em branco, espaço usado
        """
        empty_space = 0

        # Cópia do endereço inicial para percorrer a lista encadeada
        section = self.address_initial

        # Enquanto section NÃO for None
        while section is not None:
            empty_space += section.size if section.is_void() else 0
            section = section.nearby

        print(f"Espaço total: {self.max_limit}\nEspaço usado: {self.max_limit - empty_space}\nEspaço vazio: {empty_space}")

        return empty_space, self.max_limit - empty_space


# Inicializa a memória
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

    # Informando o número referente a opção
    option = int(input("Opção: "))

    # Se for 1, adicionar.
    if option == 1:
        # Informa o nome
        name = input("Digite o nome do programa: ")

        # Informa o size e verifica se ele é 2, 4, 8 ou 16.
        size = 0
        while size not in (2, 4, 8, 16):
            size = int(input("Tamanho (2, 4, 8 ou 16): "))

        # Pede a opção de encaixe válida
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

    # Se for 2, listar processos na memória.
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

    # Se for 3, remover processos na memória.
    elif option == 3:
        if m.remove(int(input("Digite o id do programa: "))):
            print("Removido com sucesso!")
        else:
            print("Id não existe!")

    # Se for 4, listar e mostrar gráfico referente a espaço usado e vazio na memória.
    elif option == 4:
        info_memory = m.show_memory_info()

        labels = f'Espaço vazio\n{info_memory[0]}M', f'Espaço usado\n{info_memory[1]}M'

        figg, axl = plt.subplots()
        axl.pie(info_memory, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        axl.axis('equal')
        plt.show()

    # Se for 5, listar processos e espaços em branco na memória.
    elif option == 5:
        m.show_memory()

    # Se for 6, Reorganiza os processo.
    elif option == 6:
        m.compress()
        print("Compactação realizada com sucesso!")

    # Se for 7, sai do programa.
    elif option == 7:
        break

    else:
        print("Comando inválido, digite novamente!")