#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Jogo da velha - Aula GIT - PEM
Descricao:
    Jogo da velha em interface grafica em linha de comando
     com dois modos: Contra o computador (utilizando o algoritmo minimax)
     e contra um adversario via rede.
TODO:
    -Tudo!
Autores:
    Aislan Jefferson - aislanjsb@gmail.com
    Douglas Nickson - douglas.nickson1@gmail.com
    Laerty Santos - laerty.santos@gmail.com
    Willian Klein - williannene1@hotmail.com
"""
# importa a biblioteca random
import random, socket, struct
#import fcntl

# Imprime na tela o tabuleiro na forma:
'''
     |   |
   a | b | c
  ___|___|___
     |   |
   d | e | f
  ___|___|___
     |   |
   g | h | i
     |   |
'''

def mostraTabuleiro(board):
    print("   |   |   ")
    print(" {} | {} | {} ".format(board[7], board[8], board[9]))
    print("___|___|___")
    print("   |   |   ")
    print(" {} | {} | {} ".format(board[4], board[5], board[6]))
    print("___|___|___")
    print("   |   |   ")
    print(" {} | {} | {} ".format(board[1], board[2], board[3]))
    print("   |   |   ")

# Essa funcao permite que o jogador escolha com qual letra ira jogar
# e no final retorna uma lista, sendo o primeiro elemento a letra do jogador
# e o segundo a letra da cpu
def escolheLetra(letter = ' '):
    while not (letter == 'X' or letter == 'O'):
        letter = str(input("Voce deseja jogar como X ou O: ")).upper()
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

# escolhe aleatoriamente quem vai ser o primeiro a jogar
def jogaPrimeiro():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

# funcao que permite ao jogar fazer seu movimento, a funcao verifica se a opcao
# escolhida pelo jogador esta entre as opcoes permitadas e verifica se o espaco esta vazio
def movimentoPlayer(board):
    move = ''
    mostraTabuleiro(theBoard)
    while move not in ('1 2 3 4 5 6 7 8 9').split() or not verificaEspacoLivre(board, int(move)):
        move = str(input('Qual a sua jogada? (1-9)'))
    return int(move)


# escreve a letra no tabuleiro
def fazJogada(board, symbol, move):
    board[move] = symbol


# funcao que pergunta se o jogador deseja jogar novamente
def jogarNovamente():
    print('Voce deseja jogar novamente? (Sim ou Nao)')
    return str(input()).lower().startswith('s')


# Essa funcao verifica todas as possibildiades de vitoria e caso tenha vencedor retorna true
def checaVencedor(board, letter):
    return ((board[7] == letter and board[8] == letter and board[9] == letter) or
            (board[4] == letter and board[5] == letter and board[6] == letter) or
            (board[1] == letter and board[2] == letter and board[3] == letter) or
            (board[7] == letter and board[4] == letter and board[1] == letter) or
            (board[8] == letter and board[5] == letter and board[2] == letter) or
            (board[9] == letter and board[6] == letter and board[3] == letter) or
            (board[7] == letter and board[5] == letter and board[3] == letter) or
            (board[9] == letter and board[5] == letter and board[1] == letter))


# Essa funcao cria uma copia do tabuleiro
def copiaBoard(board):
    copyBoard = []
    for i in board:
        copyBoard.append(i)
    return copyBoard


# Verifica se o espaco selecionado esta vazio e retorna true
def verificaEspacoLivre(board, move):
    return board[move] == ' '


# escolhe um movimento valido no tabuleiro
def escolheMovimentoAleatorio(board, movesList):
    possibleMoves = []
    for i in movesList:
        if verificaEspacoLivre(board, i):
            possibleMoves.append(i)
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


# funcao que define a jogada da cpu, utilizando AI
def movimentoCPU(board, computerLetter):
    # Dado um tabuleiro e o simbolo do jogador, a funcao determina onde jogar e retorna o movimento
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Aqui esta o algoritmo para a AI do jogo da velha
    # Primeiro, verificamos se é possivel vencer na proxima jogada
    for i in range(1, 10):
        copy = copiaBoard(board)
        if verificaEspacoLivre(copy, i):
            fazJogada(copy, computerLetter, i)
            if checaVencedor(copy, computerLetter):
                return i

                # Verifica se o jogador pode vencer na proxima jogada e, entao, o bloqueia
    for i in range(1, 10):
        copy = copiaBoard(board)
        if verificaEspacoLivre(copy, i):
            fazJogada(copy, playerLetter, i)
            if checaVencedor(copy, playerLetter):
                return i
                # Tenta ocupar algum dos cantos, se eles estiverem livres
    move = escolheMovimentoAleatorio(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Tenta ocupar o centro, se ele estiver livre
    if verificaEspacoLivre(board, 5):
        return 5

    # ocupa os lados
    return escolheMovimentoAleatorio(board, [2, 4, 6, 8])

# funcao que verifica se o tabuleiro esta completo e retorna true
def boardCheio(board):
    for i in range(1, 10):
        if verificaEspacoLivre(board, i):
            return False
    return True

def criaConexaoServ(ip,porta):
    hostConn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hostConn.bind((ip,porta))
    hostConn.listen(1)
    return hostConn

def enviarDadosStr(conexao, dado):
    return conexao.send(str(dado).encode('utf-8'))

def receberDadosStr(conexao,tamanho):
    return conexao.recv(tamanho).decode('utf-8')

def retornaIP():
    """Função que retorna o endereço IP da maquina onde está executando. O import do pacote
    micropython.fcntl foi ignorado no código e pode dar erro. Tem que ser instalado e pelo
    que vi só é possivel via comandos linux."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', 'eth0'[:15])
        )[20:24])

#Execução do Jogo

print('Bem vindo ao Game da Veia!')
PORTA = 12345

tipoGame = int(input("Voce deseja jogar: \n1 - SINGLEPLAYER \n2 - MULTIPLAYER\n"))
if tipoGame == 2:
    tipoMultiplayer =  int(input("Voce deseja ser: \n1 - CLIENTE \n2 - SERVIDOR\n"))
    if tipoMultiplayer == 2:
        ip = socket.gethostbyname(socket.gethostname())
        svcon = criaConexaoServ(ip, PORTA)
        print("Servidor iniciado no ip", ip)

# Loop principal
while (True):
    # reinicia e zera o tabuleiro, eliminando a necessidade de utilizar funcoes
    theBoard = [' '] * 10
    if tipoGame == 1 or tipoMultiplayer == 2:
        playerLetter, computerLetter = escolheLetra()
        turn = jogaPrimeiro()

    elif tipoGame == 2 and tipoMultiplayer == 1:
        ip = input("Digite o endereco IP do servidor: ")
        print("Conectando ao servidor remoto")
        conexao = socket.create_connection((ip, PORTA))
        enviarDadosStr(conexao, "1")
        assert (receberDadosStr(conexao, 1) == "1")
        print("Conectado!")
        playerLetter, computerLetter = escolheLetra(receberDadosStr(conexao, 1))
        turn = receberDadosStr(conexao, 6)

    elif tipoGame == 2 and tipoMultiplayer == 2:
        print("Aguardando jogador remoto se conectar...")
        conexao, JogadorRemotoAddr = svcon.accept()
        assert (conexao.recv(1).decode('utf-8') == "1")
        conexao.send("1".encode('utf-8'))
        print("Jogador", JogadorRemotoAddr[0], "conectado!")
        conexao.send(computerLetter.encode('utf-8'))
        conexao.send(("player" if turn != "player" else "server").encode('utf-8'))

    print('O ' + turn + ' vai jogar primeiro')
    gameIsPlaying = True

    while gameIsPlaying:
        # Vez do jogador fazer sua jogada
        if turn == 'player':
            move = movimentoPlayer(theBoard)
            fazJogada(theBoard, playerLetter, move)

            if tipoGame == 2:
                enviarDadosStr(conexao,move)

            # Verifica se ouve vencedor na jogada
            if checaVencedor(theBoard, playerLetter):
                mostraTabuleiro(theBoard)
                print('Parabens! Voce venceu o game!')
                gameIsPlaying = False
            else:
                # Verifica se o tabuleiro esta completo
                if boardCheio(theBoard):
                    print('O jogo empatou')
                    break
                else:
                    turn = 'computer'
        else:
            if tipoGame == 2:
                mostraTabuleiro(theBoard)
                print("Aguardando o jogador remoto fazer movimento...")
                move = int(receberDadosStr(conexao,1))
            else:
                move = movimentoCPU(theBoard, computerLetter)

            fazJogada(theBoard, computerLetter, move)
            # verifica se ouve vencedor na jogada
            if checaVencedor(theBoard, computerLetter):
                mostraTabuleiro(theBoard)
                print('O computador venceu o jogo :(')
                gameIsPlaying = False
            else:
                # verifica se o tabuleiro esta completo e sem vencedor
                if boardCheio(theBoard):
                    mostraTabuleiro(theBoard)
                    print('O jogo empatou!')
                    break
                else:
                    turn = 'player'
    # pergunta se deseja jogar novamente, se escolher sim o jogo e reiniciado
    if tipoGame == 2:
        conexao.close()
    if not jogarNovamente():
        break
if tipoGame == 2 and tipoMultiplayer == 2:
    svcon.close()