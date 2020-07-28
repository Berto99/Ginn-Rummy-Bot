import random
from copy import deepcopy

card_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
card_suites = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
deck = []
cards_cpy = deepcopy(deck)
hand = []
in_combination = []
not_in_combination = [0]
cards_passed = 0

# Card deck building
for i in card_suites:
    for j in card_numbers:
        deck.append([i, j])

# Random hand distributing
i = 0
while i < 10:
    candidate = random.choice(deck)
    if candidate not in hand:
        hand.append(candidate)
        deck.remove(candidate)
        i += 1

# Concrete hand distributing (Debug)
hand =[['Hearts', 11], ['Clubs', 13], ['Clubs', 1], ['Diamonds', 10], ['Hearts', 10], ['Spades', 10], ['Hearts', 1], ['Clubs', 2], ['Clubs', 5], ['Diamonds', 6]]

# Sorting hand based on suites and card size
for card_c in cards_cpy:
    for card_h in hand:
        if card_h[0] == card_c[0] and card_h[1] == card_c[1]:
            hand.remove(card_h)
            hand.insert(0, card_h)

cards_cpy.clear()


# Upon creating combination, scan the entire hand for cards to add to that combination
def combination_morph(combination, virt_hand):
    for index in range(1, len(combination)):
        card = combination[index]
        for comp_card in virt_hand:
            if combination[0] == 1:
                if card[0] == comp_card[0]:
                    if abs(card[1] - comp_card[1]) <= 1:
                        combination.append(comp_card)
                        virt_hand.remove(comp_card)
                        combination_morph(combination, virt_hand)
                        return
            if combination[0] == 2:
                if card[1] == comp_card[1]:
                    combination.append(comp_card)
                    virt_hand.remove(comp_card)
                    combination_morph(combination, virt_hand)
                    return


# Calculate the chance that the next card will be 'valuable' to the player
def chance(in_combination_local):
    chance = 0
    for c in in_combination_local:
        c1 = deepcopy(c)
        if c1[0] == 1:
            c1.remove(c1[0])
            card_in_hand = False
            max_card = max(c1, key=lambda x: x[1])
            min_card = min(c1, key=lambda x: x[1])
            if max_card[1] < 13:
                for comb in in_combination_local:
                    if [c1[0][0], max_card[1] + 1] in comb:
                        card_in_hand = True
                if not card_in_hand:
                    chance += 1/(42 - cards_passed)
            card_in_hand = False
            if min_card[1] > 1:
                for comb in in_combination_local:
                    if [c1[0][0], min_card[1] - 1] in comb:
                        card_in_hand = True
                if not card_in_hand:
                    chance += 1/(42 - cards_passed)
        if c1[0] == 2:
            c1.remove(c1[0])
            card_in_hand = False
            suites_cpy = deepcopy(card_suites)
            for card in c1:
                suites_cpy.remove(card[0])
            for comb in in_combination_local:
                if comb[0] == 1:
                    for a in range(1, len(comb)):
                        card = comb[a]
                        if card[0] in suites_cpy:
                            if card[1] == c1[0][1]:
                                card_in_hand = True
            if not card_in_hand:
                chance += (1/(42-cards_passed)) * len(suites_cpy)
    return chance * 100


# Sort the cards into card combinations - Sequential or Identical
def configure(hand_given, set_new_variables):
    virtual_hand = deepcopy(hand_given)
    current_card = []
    in_combination_local = []
    not_in_combination_local = [0]
    while 1:

        if len(virtual_hand) > 0:
            current_card = virtual_hand[0]
        else:
            break
        added = False
        virtual_hand.remove(current_card)
        # Combination[0] codes:
        # 1 - Sequential combination
        # 2 - Identical combination
        # 0 - Not in combination

        seq_hand = deepcopy(virtual_hand)
        ident_hand = deepcopy(virtual_hand)
        new_combination_seq = [1]
        new_combination_ident = [2]
        length_seq = 0
        length_ident = 0
        seq_card = []
        ident_card = []

        # Creating new seq. combination (if possible)
        for comparing_card in seq_hand:
            seq_card = comparing_card
            if current_card[0] == comparing_card[0]:
                if abs(current_card[1] - comparing_card[1]) <= 1:
                    seq_hand.remove(comparing_card)
                    new_combination_seq.append(current_card)
                    new_combination_seq.append(comparing_card)
                    combination_morph(new_combination_seq, seq_hand)
                    length_seq = len(new_combination_seq)
                    added = True
                    break

        # Creating new identical combination (if possible)
        for comparing_card in ident_hand:
            ident_card = comparing_card
            if current_card[1] == comparing_card[1]:
                ident_hand.remove(comparing_card)
                new_combination_ident.append(current_card)
                new_combination_ident.append(comparing_card)
                combination_morph(new_combination_ident, ident_hand)
                length_ident = len(new_combination_ident)
                added = True
                break

        if added:
            if length_seq >= length_ident:
                in_combination_local.append(new_combination_seq)
                virtual_hand_cpy = seq_hand
            else:
                in_combination_local.append(new_combination_ident)
                virtual_hand_cpy = ident_hand

        if not added:
            not_in_combination_local.append(current_card)

    new_hand = [in_combination_local, not_in_combination_local, chance(in_combination_local), virtual_hand]
    if set_new_variables:
        global in_combination
        in_combination = in_combination_local
        global not_in_combination
        not_in_combination = not_in_combination_local
    return new_hand


#problem when running this random hand with this random card
#need to implement method to check best combinations for both card in a newly created, so to see if comparing card has a better option
# random_card = random.choice(deck)
random_card = ['Hearts', 1]
print(random_card)
print(hand)
configure(hand, True)
print(in_combination)


current_best = []
max_chance = 0
for b in range(1, len(not_in_combination)):
    card = not_in_combination[b]
    hand_cpy = deepcopy(hand)
    hand_cpy.insert(hand_cpy.index(card), random_card)
    hand_cpy.remove(card)
    if configure(hand_cpy, False)[2] > max_chance:
        max_chance = configure(hand_cpy, False)[2]
        current_best = configure(hand_cpy, False)
cards_passed += 1
in_combination = current_best[0]
not_in_combination = current_best[1]
hand = current_best[3]

print('new combinations:')
print(in_combination)
print('best is:')
print(max_chance)
