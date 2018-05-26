#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice, shuffle
from UnoDeck import UnoDeck, Player, Cycle, GameFlow
import collections

__author__ = 'Francisco'

NAMES = ['Duplex', 'Watson', 'Cleverbot', 'Deep blue', 'Cortana', 'Siri', 'Hal 9000']


def start():
    """
    Inicia el juego y retorna el número de jugadores CPU.
    :return: x número de jugadores
    """
    print("BIENVENIDO A UNO!")
    x = -1
    while True:
        try:
            x = int(input("Ingresa la cantidad de jugadores CPU (max. 6):"))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        if x < 2 or x > 6:
            continue
        else:
            break
    return x


def cpu_players(nplayers):
    """
    Asigna a la cantidad de jugadores especificada en parámetro nombres únicos en base a la lista de nombres NAMES
    :param nplayers: número de jugadores especificado por el usuario
    :return: lista de jugadores
    """
    player_names = []
    players = []
    for i in range(nplayers):
        name = ''
        while name == '':
            name = choice(NAMES)
            for n in player_names:
                if name == n:
                    name = '';
            player_names.append(name)
        p = Player(name)
        players.append(p)
    del player_names
    for i in players:
        print(i.get_name())
    return players


def human_player():
    """
    Asigna un jugador al usuario. Solicita escribir un nombre para identificarlo.
    :return: Objeto Player (un jugador) identificado como humano
    """
    nombre = input("Escribe tu nombre: ")
    if nombre:
        h = Player(nombre)
        h.set_human()
        return h
    else:
        return human_player()


def game():
    """
    Agrupa todas las funciones que componen el juego en orden secuencial.
    :return: Un valor verdadero en caso que el usuario quiera jugar y falso para cerrar.
    """
    nplayers = start()
    players = cpu_players(nplayers)
    h = human_player()
    players.append(h)
    deck = UnoDeck()
    gf = GameFlow(deck, players)
    gf.set_game()
    gf.start_game()
    restart = input("Presiona Y para volver a jugar y cualquier otra para terminar ")
    print(restart.upper())
    if restart.lower() == 'y':
        return True
    else:
        return False


if __name__ == '__main__':
    g = True
    while g:
        g = game()
