def to_upper(lista):
    novaLista = []
    for elemento in lista:
        novaLista.append(elemento.upper())
    return novaLista

todas_palavras = []

with open('br-utf8.txt','r', encoding="utf8") as f:
    for linhas in f:
        for palavra in linhas.split():
           if(len(palavra) == 5): 
               todas_palavras.append(palavra)  

word_list = to_upper(todas_palavras)