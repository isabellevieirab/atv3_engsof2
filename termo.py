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
    return palpite not in word_list

def checa_palpite(palpite, resposta):
    respostaTratada = trata_palavra(resposta)
    resultado = []
    termoResultado = []
    for i, letra in enumerate(palpite):
        if (resposta[i] == palpite[i]) or (respostaTratada[i] == palpite[i]):
            resultado += local_correto(resposta[i])
            termoResultado.append(QUADRADOS['local_correto'])
        elif (letra in resposta) or (letra in respostaTratada):
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
    return palpite == palavraEscolhida or palpite == trata_palavra(palavraEscolhida) or trata_palavra(palpite) == palavraEscolhida or trata_palavra(palpite) == trata_palavra(palavraEscolhida)

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
    
if __name__ == '__main__':
    console = Console()
    palavraEscolhida = choice(word_list)
    console.print(MENSAGEM_INICIAL)
    console.print(INSTRUCOES)
    jogo(console, palavraEscolhida)