#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice, shuffle
import collections
import time

__author__ = 'Francisco Fuentes'

Card = collections.namedtuple('Card', ['rank', 'suit'])



class UnoDeck:
    """
    Esta clase controla el mazo de cartas de UNO.
    """
    special_color = ['+2', 'Salta', 'Reversa']
    ranks = [str(n) for n in range(0, 1)] + [str(n) for n in range(1, 10)] * 2 + special_color * 2
    suits = 'rojo azul amarillo verde'.split()
    w_ranks = ["+4", 'Comodin'] * 4
    w_suits = ["Negra"]

    def __init__(self):
        """
        Crea una instancia del objeto. Genera un mazo con las 108 cartas.
        """
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]
        wildcard = [Card(rank, suit) for suit in self.w_suits
                    for rank in self.w_ranks]
        for wc in wildcard:
            self._cards.append(wc)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(deck, position, card):
        deck._cards[position] = card

    def get_deck(self):
        """
        Retorna un mazo.
        """
        return self._cards;

    def refill_deck(self, cards):
        """
        En caso de que el mazo quede sin cartas,
        rellena el mazo (self._cards) con las cartas ya jugadas
        """
        self._cards.extend(cards)


class Player:
    """
    Objeto que es capaz de jugar una partida de Uno.
    """

    def __init__(self):
        """
        Inicializa un jugador de Uno. Devuelve un objeto Player.
        :return:
        """
        self._hand = []
        self._value = []
        self._name = ''
        self._isHuman = False

    def __init__(self, name):
        """
        Inicializa un jugador de uno con un parámetro name igual al nombre que queremos que tenga.
        Devuelve un objeto Player.
        :param name:
        :return:
        """
        self._hand = []
        self._value = []
        self._name = name
        self._isHuman = False

    def set_hand(self, deck):
        """
        Toma 7 cartas del mazo para empezar a jugar. El parámetro deck es el mazo y las cartas tomadas de éste
        son escogidas al azar.
        :param deck:
        :return:
        """
        self._hand = []
        for i in range(7):
            c = choice(deck)
            self._hand.append(c)
            # cambiar lo de abajo
            deck._cards.remove(c)
        self.set_values(deck)

    def get_hand(self):
        """
        Devuelve el contenido de la mano de cartas del jugador.
        :return:
        """
        return self._hand

    def set_name(self, name):
        """
        Da un nombre al jugador.
        :param name:
        :return:
        """
        self._name = name

    def get_name(self):
        """
        Devuelve el nombre del jugador.
        :return:
        """
        return self._name

    def set_human(self):
        self._isHuman = True

    def isHuman(self):
        return self._isHuman

    def check_card(self, card):
        """
        Recibe un parámetro que contiene la carta en la mesa de juego. En base a ella revisa si su mano de cartas
        contiene una carta jugable.
        :param card: Carta en juego (active_card)
        :return: Una lista de cartas jugables
        """
        playable = list(filter(lambda c: c.rank == card.rank or c.suit == card.suit or c.suit == 'Negra', self._hand))
        return playable

    def set_values(self, playable):
        """
        En base a las cartas jugables de check_card devuelve una lista con los valores de cada una de ellas.
        :param playable:
        :return:
        """
        values = []
        for c in playable:
            if c.rank.isdigit():
                values.append(int(c.rank))
            elif c.suit != 'Negra':
                values.append(20)
            else:
                values.append(50)
        return values

    def highest(self, playable):
        """
        En base a las cartas jugables calcula cuál es la carta más valiosa.
        :param playable:
        :return:
        """
        values = self.set_values(playable)
        pos = -1
        if values:
            maximum = max(values)
            for i in range(len(values)):
                if values[i] == maximum:
                    pos = i
        for i in range(len(self._hand)):
            if self._hand[i] == playable[pos]:
                return i

    def play_card(self, card) -> Card:
        """
        Devuelve la carta más viable para jugar y la retira de su mano.
        Si no encuentra ninguna devuelve False
        :rtype : list
        """
        playable = self.check_card(card)
        if playable:
            position = self.highest(playable)
            hand = self._hand
            return hand.pop(position)
        return False

    def pick_card(self, deck):
        """
        Recibe un parámetro deck con un mazo en juego y saca una carta de este mazo.
        :return:
        """
        self._hand.append(deck.pop())

    def __len__(self):
        return len(self._hand)

    def __getitem__(self, position):
        return self._hand[position]


class Cycle:
    """
    Permite crear un ciclo de juego que recorra la lista de Player incluyendo las operaciones propias del juego Uno
    como la reversa y el salto (skip)
    """

    def __init__(self, player_list):
        """
        Inicializa el ciclo de juego con una lista de jugadores (de clase Player)
        :param player_list:
        :return:
        """
        self._players = player_list
        self._position = None
        self._isReverse = False

    def __next__(self):
        """
        Permite iterar en un cíclo continuo de manera flexible.
        :return:
        """
        if self._position is None:
            self._position = -1 if self._isReverse else 0
        elif self._position == len(self._players) - 1 and not self._isReverse:
            self._position = 0
        elif self._position == 0 and self._isReverse:
            self._position = len(self._players) - 1
        else:
            self._position = self._position + self._delta()
        return self._players[self._position]

    def _delta(self):
        """
        Es el paso en el cual avanza el puntero del ciclo (hacia atrás -1 o hacia adelante 1)
        :return:
        """
        return -1 if self._isReverse else 1

    def get_pos(self, pos):
        """
        Entrega un objeto obtenida la posición.
        :param pos:
        :return:
        """
        return self._players[pos]

    def get_next(self):
        """
        Obtiene el siguiente objeto en la iteración sin afectar al __next__.
        :return player:
        """
        if self._position == len(self._players) - 1 and not self._isReverse:
            return self._players[0]
        elif self._position == 0 and self._isReverse:
            return self._players[len(self._players) - 1]
        else:
            return self._players[self._position + self._delta()]

    def cur_pos(self):
        """
        Devuelve la posición actual del ciclo.
        :return int:
        """
        return self._position

    def reverse(self):
        """
        Revierte el orden del iterable.
        """
        self._isReverse = not self._isReverse


class GameFlow:
    def __init__(self, deck, players):
        """
        Recibe un mazo de cartas y una lista de jugadores. Devuelve un objeto.
        :param deck:
        :param players:
        :return:
        """
        self._deck = UnoDeck()
        self._players = players
        self._discard = []
        self._game_cycle = None

    def __getattribute__(self, *args, **kwargs):
        return super().__getattribute__(*args, **kwargs)

    def set_game(self):
        """
        Inicia el juego mezclando las cartas, entregando las cartas a los jugadores y creando el ciclo de juego
        :return:
        """
        shuffle(self._deck)
        for p in self._players:
            p.set_hand(self._deck)
        self._discard = [self._deck.get_deck().pop()]
        self._game_cycle = Cycle(self._players)
        # p = list(map(lambda x: print(x.get_name(), " parte con: ", x.get_hand()), self._players))


    def eval_card(self, carta, current_player, next_player):

        """
        Evalúa una carta puesta en juego por un jugador para producir los efectos esperados del juego
        :param carta:
        :return: None
        """
        print("La respuesta de ", current_player.get_name(), " es ", carta)
        if carta.rank == 'Salta':
            self._game_cycle.__next__()
            print(current_player.get_name(), " juega carta y hace perder turno a su vecino.")
            if next_player.isHuman():
                input()
        elif carta.rank == 'Reversa':
            self._game_cycle.reverse()
            print("El sentido del juego se revierte!")
        elif carta.rank == '+2':
            new_cards = self._deck.get_deck()[-2:]
            del self._deck.get_deck()[-2:]
            next_player.get_hand().extend(new_cards)
            print(next_player.get_name(), " recibe 2 cartas y pierde su turno!")
            if next_player.isHuman():
                input()
            self._game_cycle.__next__()
        elif carta.rank == '+4':
            new_cards = self._deck.get_deck()[-4:]
            del self._deck.get_deck()[-4:]
            next_player.get_hand().extend(new_cards)
            print(next_player.get_name(), " recibe 4 cartas y pierde su turno!")
            if next_player.isHuman():
                input()
            self._game_cycle.__next__()
        else:
            print(current_player.get_name(), "juega rango:", carta.rank, "color:", carta.suit)

        if carta.suit == 'Negra':
            del self._discard[-1:]
            new_card = None
            new_color = ''
            suits = UnoDeck.suits
            if current_player.isHuman():
                while not new_color:
                    for suit in suits:
                        print("Color: ",suit,"digita: ",suits.index(suit))
                    color_input = input("Selecciona el nuevo color:")
                    color_choice = int(color_input) if color_input.isdigit() else -1
                    if color_choice >= 0 and color_choice < len(suits):
                        new_color = suits[color_choice]
                        new_card = Card(carta.rank, new_color)
                    else:
                        continue
            else:
                new_color = choice(suits)
                new_card = Card(carta.rank, new_color)

            self._discard.append(new_card)
            print(current_player.get_name(), " ha elegido ", new_color)




    def human_turn(self, current_player, active_card, keep, carta, t):
        current_hand = current_player.get_hand()
        next_player = self._game_cycle.get_next()
        print("Tienes estas cartas para jugar: ")
        for i in current_hand:
            print("Rango: ", i.rank, "Color: ", i.suit, "Digita: ", current_hand.index(i))
        n = input("Digita el número de la carta, d para sacar una carta del mazo o p para pasar:")
        if n.isnumeric() and int(n) <= len(current_hand) - 1:
            v = int(n)
            for i in current_player.check_card(active_card):
                if current_player.get_hand()[v] == i:
                    carta = i
                    current_player.get_hand().pop(v)
                    keep = False
                    self._discard.append(carta)
                    self.eval_card(carta, current_player, next_player)
                    break
            # self._discard.append(carta)
            # self.eval_card(carta, current_player, next_player)
        elif n.lower() == 'd':
            if not self._deck.get_deck():
                self._deck.refill_deck(self._discard)
            current_player.pick_card(self._deck.get_deck())
            print(current_player.get_name(),"toma una carta")
        elif n.lower() == 'p':
            if t == 0:
                if not self._deck.get_deck():
                    self._deck.refill_deck(self._discard)
                current_player.pick_card(self._deck.get_deck())
                print(current_player.get_name(),"toma una carta")
            keep = False

        return keep

    def start_game(self):
        """
        Desarrolla el juego con sus turnos hasta que haya un ganador.
        :param game_cycle:
        :return: None
        """
        print("COMIENZA EL JUEGO!\n")
        while True:
            time.sleep(5)
            current_player = self._game_cycle.__next__()
            active_card = self._discard[len(self._discard) - 1]
            carta = ''
            print("\nEl turno es de ", current_player.get_name())
            print("La carta sobre la mesa es Rango: ", active_card.rank, "color: ", active_card.suit)
            if current_player.isHuman():
                print("TE TOCA!\n")
                keep = True
                t = 0
                while keep:
                    keep = self.human_turn(current_player, active_card, keep, carta, t)
                    t += 1
            else:
                carta = current_player.play_card(active_card)

            next_player = self._game_cycle.get_next()
            if carta:
                self._discard.append(carta)
                self.eval_card(carta, current_player, next_player)
            elif not carta and not current_player.isHuman:
                if self._deck:
                    current_player.pick_card(self._deck.get_deck())
                else:
                    # si no hay cartas en el mazo lo rellena con las cartas ya jugadas
                    self._deck.refill_deck(self._discard)
                    current_player.pick_card(self._deck.get_deck())
                print(current_player.get_name(), "toma una carta")
                carta = current_player.play_card(active_card)
                if carta:
                    self._discard.append(carta)
                    self.eval_card(carta, current_player, next_player)
            cards_left = len(current_player.get_hand())
            if cards_left > 1:
                print("A",current_player.get_name(),"le quedan",cards_left,"cartas")
            elif len(current_player.get_hand()) == 1:
                print("\nUNO!", current_player.get_name(), " tiene sólo 1 carta!!!!\n")
            elif len(current_player.get_hand()) == 0:
                print(current_player.get_name(), " ha ganado!")
                return False
