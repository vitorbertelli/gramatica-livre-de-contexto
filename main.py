from typing import Self

class Gramatica:
  """
  Classe para representar uma gramática formal.

  Atributos:
    - variaveis: list - uma lista de variáveis da gramática
    - inicial: str - a variável inicial da gramática
    - producoes: dict - um dicionário onde a chave é uma variável e o valor é uma lista de produções
  """

  def __init__(self, variaveis: list, inicial: str, producoes: dict):
    self.variaveis = variaveis
    self.inicial = inicial
    self.producoes = producoes

  def simplificar(self) -> type[Self]:
    """
    Método para simplificar uma gramática, eliminando produções inúteis, vazias e unitárias.
    Saída:
      Gramatica - um novo objeto de gramática simplificado
    """
    resultado = self.eliminar_producoes_vazias()
    resultado = resultado.eliminar_producoes_unidades()
    resultado = resultado.eliminar_producoes_inuteis()
    return resultado

  def eliminar_producoes_inuteis(self) -> type[Self]:
    """
    Método para eliminar produções inúteis de uma gramática.
    Uma variável pode ser considerada inútil por duas razões:
      - A variável não é geradora de uma sentença (cadeia de terminais), pois cria-se um ciclo
      - A variável não é alcançável a partir do símbolo inicial

    Saída:
      Gramatica - um novo objeto de gramática sem as produções inúteis
    """

    # Primeira etapa - Realiza a verificação das variáveis geradoras de terminais
    variaveis_uteis = list()
    for variavel in self.variaveis:
      if self.__verificar_terminal(variavel):
        variaveis_uteis.append(variavel)

    # Segunda etapa - Realiza a verificação das variáveis alcançáveis a partir do símbolo inicial e com base nas variáveis geradoras de terminais
    pilha = list()
    pilha.append(self.inicial)
    variaveis_alcancaveis = list()
    while pilha != []:
      variavel = pilha.pop()
      variaveis_alcancaveis.append(variavel)
      for producao in self.producoes[variavel]:
        if all(simbolo in variaveis_uteis or simbolo not in self.variaveis for simbolo in producao):
          for simbolo in producao:
            if simbolo in variaveis_uteis and simbolo not in variaveis_alcancaveis:
              pilha.append(simbolo)

    # Remove as produções inúteis com base nas variáveis alcançáveis
    producoes_uteis = dict()
    for variavel in variaveis_alcancaveis:
      producoes_uteis[variavel] = list()
      for producao in self.producoes[variavel]:
        if all(simbolo in variaveis_alcancaveis or simbolo not in self.variaveis for simbolo in producao):
          producoes_uteis[variavel].append(producao)

    variaveis_alcancaveis = list(set(variaveis_alcancaveis)) # Remove duplicatas

    resultado = Gramatica.nova(variaveis_alcancaveis, self.inicial, producoes_uteis)
    return resultado

  def __verificar_terminal(self, variavel: str, visitados=None) -> bool:
    """
    Verifica se uma variável gera um terminal, seja diretamente ou indiretamente.

    Entrada:
      variavel: str - uma variável da gramática a ser verificada
      visitados: list - lista de variáveis verificadas para evitar ciclos, usado para recursão

    Saída: 
      bool - True se a variável gera um terminal, False caso contrário
    """

    if visitados is None:
      visitados = list()
    
    if variavel in visitados:
      return False
    else:
      visitados.append(variavel)

    if variavel in self.producoes:
      for producao in self.producoes[variavel]:
        if all(simbolo not in self.variaveis or self.__verificar_terminal(simbolo, visitados) for simbolo in producao):
          return True
      
    return False

  def eliminar_producoes_vazias(self) -> type[Self]:
    """
    Método para eliminar produções vazias de uma gramática.
    Uma produção é considerada vazia se ela é da forma A -> h, onde h é a cadeia vazia.
    
    Saída:
      Gramatica - um novo objeto de gramática sem as produções vazias
    """
    
    resultado = Gramatica.nova(self.variaveis, self.inicial, self.producoes)

    # Primeira etapa - Encontrar as variáveis anuláveis:
    # a) Para todo A tal que existe A -> h, incluir A em Vn (representado por variaveis_anulaveis)
    variaveis_anulaveis = list()
    for variavel in self.variaveis:
      for producao in self.producoes[variavel]:
        if producao == "h":
          variaveis_anulaveis.append(variavel)

    # b) Para todo B tal que existe a produção B -> A1A2...An, onde Ai pertencentes todos a Vn, incluir B em Vn
    for variavel in self.variaveis:
      for producao in self.producoes[variavel]:
        if producao in variaveis_anulaveis:
          variaveis_anulaveis.append(variavel)

    # Segunda etapa - Substituição de produções com variáveis anuláveis
    for variavel in self.variaveis:
      for producao in self.producoes[variavel]:
        # Aplicar o método de retirada da produção vazia para cada produção que contém variáveis anuláveis
        # print(producao + " in ")
        # print(variaveis_anulaveis)
        if producao in variaveis_anulaveis:
          # print("true")
          if producao in resultado.producoes[variavel]: 
            resultado.producoes[variavel].remove(producao)
        elif any(simbolo in variaveis_anulaveis for simbolo in producao):
          combinacoes = self.__gerar_combinacoes(producao, variaveis_anulaveis) 
          resultado.producoes[variavel] = combinacoes

    return resultado

  def __gerar_combinacoes(self, producao: str, variaveis_anulaveis: list) -> list:
    """
    A partir da produção e do conjunto de variáveis anuláveis, gera-se um conjunto de combinações de produções
    de tal forma que, após o processo, as produções não sejam mais anuláveis.
    A função realiza os seguintes passos:
      - Inicializa um conjunto de combinações com a produção original
      - Remove todas as variáveis anuláveis da produção
      - Para cada variável anulável removida, gera-se uma nova produção sem ela
      - Adiciona a nova produção ao conjunto de combinações
      - Repete o processo para cada nova produção gerada, até que não existam mais variáveis anuláveis dentro das combinações
    
    Entrada:
      - producao: str - uma produção da gramática
      - variaveis_anulaveis: list - uma lista de variáveis anuláveis
    
    Saída:
      - list - uma lista de combinações de produções sem variáveis anuláveis
    """

    combinacoes = set() # Foi utilizado um conjunto para evitar duplicatas
    combinacoes.add(producao)

    for i in range(len(producao)):
      if producao[i] in variaveis_anulaveis:
        nova_combinacao = list(producao)
        nova_combinacao.pop(i)
        nova_producao = "".join(nova_combinacao)
        if nova_producao != "":
          combinacoes.add(nova_producao)
          combinacoes.update(self.__gerar_combinacoes(nova_producao, variaveis_anulaveis))
    
    return list(combinacoes) # Converte o conjunto para uma lista para facilitar a manipulação na função original

  def eliminar_producoes_unidades(self) -> type[Self]:
    """
    Método para remoção das produções unitárias produções unitárias de uma gramática. 
    Para qualquer produção da forma A -> B, onde B é uma variável, a produção é considerada unitária.
    Para qualquer (A, B) tal que possa encontrar A -> B usando apenas produções unidade é um par unidade.

    Saída:
      - Gramatica - um novo objeto de gramática sem as produções unitárias
    """
    resultado = Gramatica.nova(self.variaveis, self.inicial, self.producoes)

    # Primeira etapa - Eliminar qualquer produção da forma A -> A
    for variavel in self.variaveis:
      resultado.producoes[variavel] = [producao for producao in self.producoes[variavel] if producao != variavel]

    # Segunda etapa - Criar um conjunto de produções não-unidades
    producoes_nao_unidades = dict()
    for variavel in resultado.variaveis:
      producoes_nao_unidades[variavel] = list()
      for producao in resultado.producoes[variavel]:
        if len(producao) != 1 or producao not in self.variaveis:
          producoes_nao_unidades[variavel].append(producao)

    # Terceira etapa - Procurar por pares unidades
    pares_unidades = list()
    for variavel in resultado.variaveis:
      for producao in resultado.producoes[variavel]:
        if len(producao) == 1 and producao in self.variaveis:
          pares_unidades.append((variavel, producao))
 
    # Verificar Conexões indiretas nos pares unidades
    for variavel, producao in pares_unidades:
      conexoes_indireta = list(filter(lambda par: par[0] == producao, pares_unidades))
      for conexao in conexoes_indireta:
        if conexao[1] != variavel and (variavel, conexao[1]) not in pares_unidades:
          pares_unidades += [(variavel, conexao[1])]

    # Quarta etapa - Introduzir as derivações que substituem os pares unidade Introduzir as derivações que substituem os pares unidade
    for variavel, producao in pares_unidades:
      if producao in resultado.producoes[variavel]:
        resultado.producoes[variavel].remove(producao)
      if producoes_nao_unidades[producao]:
        resultado.producoes[variavel] += producoes_nao_unidades[producao]

    return resultado
  
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False  

    if sorted(self.variaveis) != sorted(other.variaveis):
      return False

    if self.inicial != other.inicial:
      return False

    if self.producoes.keys() != other.producoes.keys():
      return False

    for key in self.producoes:
      if sorted(self.producoes[key]) != sorted(other.producoes[key]):
        return False

    return True

  
  def __repr__(self):
    return f"Gramatica({self.variaveis}, {self.inicial}, {self.producoes})"

  @classmethod
  def carregar(cls, caminho: str) -> type[Self]:
    """
    Carrega um arquivo de texto, contendo uma gramática, fornecido e retorna uma instância dessa
    classe representando essa gramática. O arquivo deve seguir o seguinte formato:
      1ª linha: uma lista de variáveis separadas por espaço
      2ª linha: a variável inicial
      3ª em diante: uma produção por linha, no formato "variável produção", por exemplo: "S aSb"
    """
    with open(caminho, "r") as arquivo:
      variaveis = arquivo.readline().strip().split(" ")
      inicial = arquivo.readline().strip()
      producoes = dict()
      for producao in arquivo.readlines():
        variavel, producao = producao.strip().split(" ")
        if variavel not in producoes:
          producoes[variavel] = list()
        producoes[variavel].append(producao)
      return cls(variaveis, inicial, producoes)
  
  @classmethod
  def nova(cls, variaveis: list, inicial: str, producoes: dict) -> type[Self]:
    """
    Cria uma nova instância dessa classe com os parâmetros fornecidos.
    """
    return cls(variaveis, inicial, producoes)

  def salvar(self, caminho: str) -> None:
    """
    Salva um objeto dessa classe em um arquivo de texto, no mesmo formato que o método carregar.
    """
    with open(caminho, "w") as arquivo:
      arquivo.write(" ".join(self.variaveis) + "\n")
      arquivo.write(self.inicial + "\n")
      for variavel, producoes in self.producoes.items():
        for producao in producoes:
          arquivo.write(f"{variavel} {producao}\n")


if __name__ == "__main__":
  gramatica = Gramatica.carregar("gramaticas/gramatica_para_simplificar.txt")
  resultado = gramatica.simplificar()
  resultado.salvar("gramaticas/gramatica_simplificada.txt")