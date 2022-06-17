import unicodedata
from rich.prompt import Prompt
from rich.console import Console
from random import choice
from words import word_list

QUADRADOS = {
    'local_correto': '🟩',
    'letra_correta': '🟨',
    'letra_incorreta': '⬛'
}

def local_correto(letra):
    return f'[black on green]{letra}[/]'

def letra_correta(letra):
    return f'[black on yellow]{letra}[/]'

def letra_incorreta(letra):
    return f'[black on white]{letra}[/]'

def trata_palavra(palavra):
    return ''.join(ch for ch in unicodedata.normalize('NFKD', palavra) if not unicodedata.combining(ch))

def tentativa_repetida(palpite, tentativas):
    return palpite in tentativas
    
def tamanho_incorreto(palpite):
    return len(palpite) != 5

def palavra_invalida(palpite):
    word_list_tratada = [trata_palavra(palavra) for palavra in word_list] #map(trata_palavra, word_list)
    #print(word_list_tratada)
    #print(palpite)
    return trata_palavra(palpite) not in word_list_tratada

def acertou_letra_errou_local(letra, resposta, arrayCountLetras):
    indiceLetra = trata_palavra(resposta).find(trata_palavra(letra))
    if (letra in resposta) or (letra in trata_palavra(resposta)):
        arrayCountLetras[indiceLetra] = arrayCountLetras[indiceLetra] - 1
        return (arrayCountLetras[indiceLetra]) >= 0
    else:
        return False

def conta_letras(palavra):
    palavra = trata_palavra(palavra)
    array = []
    for letra in palavra:
        array.append(palavra.count(letra))
    return array

def checa_palpite(palpite, resposta):
    resultado = []
    termoResultado = []
    arrayCountLetras = conta_letras(resposta)

    for i, letra in enumerate(palpite):
        if acertou(palpite[i],resposta[i]):#(resposta[i] == palpite[i]) or (respostaTratada[i] == palpite[i]):
            aux = trata_palavra(resposta).find(trata_palavra(letra))
            arrayCountLetras[aux] = arrayCountLetras[aux] - 1
            resultado += local_correto(resposta[i])
            termoResultado.append(QUADRADOS['local_correto'])
        elif acertou_letra_errou_local(letra, resposta, arrayCountLetras):#(letra in resposta) or (letra in respostaTratada):#arrayCountLetras
            resultado += letra_correta(letra)
            termoResultado.append(QUADRADOS['letra_correta'])
        else:
            resultado += letra_incorreta(letra)
            termoResultado.append(QUADRADOS['letra_incorreta'])
    return ''.join(resultado), ''.join(termoResultado)

MENSAGEM_INICIAL = f'\n[white on blue] BEM VINDO AO TERMO [/]\n'
INSTRUCOES = "Você deve tentar adivinhar a palavra correta que contém até 5 letras.\n - Letras corretas no local correto terão a cor "+local_correto('verde')+".\n - Letras corretas no local incorreto terão a cor "+letra_correta('amarela')+".\n - Letras incorretas terão a cor "+letra_incorreta('branca')+".\nBoa sorte!\n"
TEXTOPALPITE = "\nEntre com seu palpite"
TENTATIVAS = 6


def palpite_invalido(palpite, tentativas):
    if tamanho_incorreto(palpite):
        console.print("[red]A palavra precisa ter 5 letras!\n[/]")
        return True
    elif tentativa_repetida(palpite, tentativas):
        console.print('[red]Você já chutou essa palavra!\n[/]')
        return True
    elif palavra_invalida(palpite):
        console.print('[red]Essa palavra não é válida!\n[/]')
        return True
    else:
        return False

def acertou(palpite, palavraEscolhida):
    palpiteIgualPalavra = palpite == palavraEscolhida
    palpiteIgualPalavraTratada = palpite == trata_palavra(palavraEscolhida) 
    palpiteTratadoIgualPalavra = trata_palavra(palpite) == palavraEscolhida
    palpiteTratadoIgualPalavraTratada = trata_palavra(palpite) == trata_palavra(palavraEscolhida)
    return palpiteIgualPalavra or palpiteIgualPalavraTratada or palpiteTratadoIgualPalavra or palpiteTratadoIgualPalavraTratada

def fim_do_jogo(palpite, palavraEscolhida, tentativas):
    if acertou(palpite, palavraEscolhida):
        console.print(f"\n[green]TERMO {len(tentativas)}/{TENTATIVAS}[/]\n")
        return True
    elif len(tentativas) == TENTATIVAS:
        console.print(f"\n[red]TERMO X/{TENTATIVAS}[/]")
        console.print(f'\n[green]A palavra era: {palavraEscolhida}[/]')
        return True
    else:
        return False

def jogo(console, palavraEscolhida):
    tentativas = []
    termoCompleto = []
    palavrasAdivinhadas = []
    palpite = ''
    while not fim_do_jogo(palpite, palavraEscolhida, tentativas):
        palpite = Prompt.ask(TEXTOPALPITE).upper()
        while palpite_invalido(palpite, tentativas):
            palpite = Prompt.ask(TEXTOPALPITE).upper()
        tentativas.append(palpite)
        resposta, resultado_wordle = checa_palpite(palpite, palavraEscolhida)
        palavrasAdivinhadas.append(resposta)
        termoCompleto.append(resultado_wordle)
        console.print(*palavrasAdivinhadas, sep="\n")
    console.print(*termoCompleto, sep="\n")
    
console = Console()
if __name__ == '__main__':
    palavraEscolhida = choice(word_list)
    console.print(MENSAGEM_INICIAL)
    console.print(INSTRUCOES)
    #console.print(palavraEscolhida)
    jogo(console, palavraEscolhida)