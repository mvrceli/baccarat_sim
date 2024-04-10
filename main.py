import random
card_values = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 0, 'J': 0, 'Q': 0, 'K': 0
}

def create_deck(num_decks):

    deck = []
    for _ in range(num_decks):
        for card, value in card_values.items():
            deck.extend([card] * 4)
    random.shuffle(deck)
    return deck

# Betting strategy: 
def bet(balance, previous_winner, previous_bet, hands_played):
    if hands_played < 3 or previous_bet is None:
        return 0, None 
    elif previous_winner is None or previous_winner == 'Tie':
        return 10, 'Player'  
    elif previous_bet > 0:
        if balance >= previous_bet * 2:
            return previous_bet * 2, previous_winner  
        else:
            return balance, previous_winner 
    else:
        return 10, previous_winner  
    
def play_baccarat(num_decks, num_hands, initial_balance):
    deck = create_deck(num_decks)
    original_deck_size = len(deck)
    reshuffle_threshold = original_deck_size * 0.25
    player_wins = 0
    banker_wins = 0
    ties = 0
    hands_played = 0
    balance = initial_balance
    previous_winner = None
    previous_bet = None
    skip_next_hand = False
    while hands_played < num_hands:
        if len(deck) < reshuffle_threshold:
            deck = create_deck(num_decks)

        if skip_next_hand:
            skip_next_hand = False
            continue

        bet_amount, bet_on = bet(balance, previous_winner, previous_bet, hands_played)

        player_hand = []
        banker_hand = []
        
        # Deal initial cards
        player_hand.append(deck.pop())
        banker_hand.append(deck.pop())
        player_hand.append(deck.pop())
        banker_hand.append(deck.pop())
        
        # Calculate hand values
        player_value = sum([card_values[card] for card in player_hand]) % 10
        banker_value = sum([card_values[card] for card in banker_hand]) % 10
        
        # Determine if a third card needs to be drawn
        if player_value <= 5 and len(deck) > 0:
            player_hand.append(deck.pop())
            player_value = sum([card_values[card] for card in player_hand]) % 10
        
        if banker_value <= 2 and len(deck) > 0:
            banker_hand.append(deck.pop())
            banker_value = sum([card_values[card] for card in banker_hand]) % 10
        elif banker_value == 3 and player_hand[-1] != '8' and len(deck) > 0:
            banker_hand.append(deck.pop())
            banker_value = sum([card_values[card] for card in banker_hand]) % 10
        elif banker_value == 4 and player_hand[-1] in ['2', '3', '4', '5', '6', '7'] and len(deck) > 0:
            banker_hand.append(deck.pop())
            banker_value = sum([card_values[card] for card in banker_hand]) % 10
        elif banker_value == 5 and player_hand[-1] in ['4', '5', '6', '7'] and len(deck) > 0:
            banker_hand.append(deck.pop())
            banker_value = sum([card_values[card] for card in banker_hand]) % 10
        elif banker_value == 6 and player_hand[-1] in ['6', '7'] and len(deck) > 0:
            banker_hand.append(deck.pop())
            banker_value = sum([card_values[card] for card in banker_hand]) % 10

        # Determine the winner
        if player_value > banker_value:
            player_wins += 1
            if bet_on == 'Player':
                balance += bet_amount
                previous_bet = None
                skip_next_hand = True
            else:
                balance -= bet_amount
                previous_bet = bet_amount
            previous_winner = 'Player'
        elif player_value < banker_value:
            banker_wins += 1
            if bet_on == 'Banker':
                balance += bet_amount
                previous_bet = None
                skip_next_hand = True
            else:
                balance -= bet_amount
                previous_bet = bet_amount
            previous_winner = 'Banker'
        else:
            ties += 1
            if bet_on == 'Tie':
                balance -= bet_amount
                previous_bet = bet_amount
            previous_winner = 'Tie'

        print(f"Round: {hands_played+1}, Winner: {previous_winner}, Bet on: {bet_on}, Bet amount: {bet_amount}, Balance: {balance}")

        hands_played += 1
    return (player_wins, banker_wins, ties, balance)

num_decks = 6
num_hands = 100
initial_balance = 1000
result = play_baccarat(num_decks, num_hands, initial_balance)
print(result)