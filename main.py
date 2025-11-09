import art
import random
import cards
print(art.logo)

def draw_card():
    """This function returns a random card in a list format, eg: ['J' , '♥️']"""
    new_card = [random.choice(cards.card_number), random.choice(cards.card_type)]
    return new_card

def get_card_value(current_card):
    """This function returns the value in points of a card"""
    #print(current_card[0])
    current_card_value = cards.card_value[current_card[0]]
    #print(f"** The value of the card {''.join(current_card)} is {current_card_value} points.")
    return current_card_value

def count_aces(user_hand):
    number_of_aces = 0
    for card in user_hand:
        if card[0] == '1':
            number_of_aces += 1
    return number_of_aces

def calculate_hand_value(user_hand):
    total_hand_value = 0
    nb_of_aces = count_aces(user_hand)

    for count in range(0, len(user_hand)):
        total_hand_value += get_card_value(user_hand[count])

    #print(f"Total hand value: {total_hand_value}")

    if nb_of_aces > 0 and total_hand_value > 21:
        print(f"Found {nb_of_aces} aces, reducing hand value...")

        # Case: all aces counted as 1, but still above 21
        if total_hand_value - (nb_of_aces * 10) > 21:
            total_hand_value -= (nb_of_aces * 10)
            print(f"Even if we count all your aces as 1, you hand is worth {total_hand_value}, which is still above 21")

        # Case: as we know we can't be in the scenario of all aces reduced to 1 makes us continue, we reduce aces one by one until the total is below 21
        else:
            ace_index = 1
            while total_hand_value > 21:
                """This loop ensures to reduce progressively aces values until the hand value is below 21 - we are sure to go below 21 because we already checked the case
                where reducing all aces to 1 wouldn't make the value goes below 21"""
                print(f"Reduced ace {ace_index}/{nb_of_aces} at value 1 instead of 11. Total hand value is {total_hand_value} - 10 = {total_hand_value - 10}")
                total_hand_value -= 10
                ace_index += 1

    return total_hand_value

def initialize_game(user):
    initial_hand_value = 0
    u_hand = [draw_card(), draw_card()]

    if user == "Computer":
        print(f"{user}'s hand: ??, {''.join(u_hand[1])}")
    else:
        print(f"{user}'s hand: {' '.join(''.join(card) for card in u_hand)}")

    initial_hand_value += calculate_hand_value(u_hand)
    if user == "Player":
        #print(f"{user}'s hand value is: {initial_hand_value}")
        if (get_card_value(u_hand[0]) + get_card_value(u_hand[1])) == 21:
            print("Blackjack!!")

    return u_hand


should_play = ""
while should_play != "n":
    should_play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ")

    if should_play == "n":
        print(20 * "\n")
        print("Thanks for playing 🧀 Refervesco's Blackjack! 🃏")
        print(5 * "\n")

    elif should_play == "y":
        player = "Player"
        computer = "Computer"

        print(20 * "\n")
        print("Initializing game...")
        print("--------------------------")
        computer_hand = initialize_game(user = computer)
        print("--------------------------")
        player_hand = initialize_game(user = player)
        print("--------------------------")

        card_count = 0
        current_hand_value = 0
        for card in player_hand:
            current_hand_value += get_card_value(player_hand[card_count])
            card_count += 1

        print(f"Your hand value is: {current_hand_value}")
        playing = True
        additional_card = 0
        hand_frozen = False # sets when the hand of the player is defined, to avoid going through the computer turn.

        while playing:
            continue_drawing = input("Do you want to draw another card? 'y' or 'n'")
            if continue_drawing == "n":
                print("\n")
                print(f"You decided to stop at {current_hand_value}, with the hand {' '.join(''.join(card) for card in player_hand)}")
                hand_frozen = True
                playing = False

            elif continue_drawing == "y":
                additional_card += 1
                player_hand.append(draw_card())
                print(f"You draw a {''.join(player_hand[1 + additional_card])}")
                print(f"Your hand is now: {' '.join(''.join(card) for card in player_hand)}")
                current_hand_value = calculate_hand_value(player_hand)
                print(f"Your new hand value is: {current_hand_value}.")

            else:
                print("Wrong input")

            if current_hand_value > 21:
                print(f"****** Your hand reached {current_hand_value}, which exceeds 21. You LOOSE. ******")
                playing = False

        # out of the while playing, resolving the computer hand...
        computer_card_count = 0
        current_computer_hand_value = 0

        # calculating computer's hand value
        for card in computer_hand:
            current_computer_hand_value += get_card_value(computer_hand[computer_card_count])
            computer_card_count += 1

        if hand_frozen:
            print("############")
            print(f"The computer reveals his hands: {' '.join(''.join(card) for card in computer_hand)}")
            print(f"Computer's hand value is {calculate_hand_value(computer_hand)}")

            while current_computer_hand_value < 17:
                computer_hand.append(draw_card())
                print(f"The computer draws a new card...")
                print(f"The computer's hand is now: {' '.join(''.join(card) for card in computer_hand)}")
                current_computer_hand_value = calculate_hand_value(computer_hand)
                print(f"The new computer's hand value is: {current_computer_hand_value}")

            if 17 <= current_computer_hand_value <= 21:
                if current_computer_hand_value < current_hand_value:
                    print(f"****** 🎉 You have a better hand than the computer (you have {current_hand_value}, he has {current_computer_hand_value}), you WIN 🎉. ******")

                if current_computer_hand_value == current_hand_value:
                    print(f"****** You and the computer have the same hand value ({current_hand_value} points). It's a SPLIT. ******")

                if current_computer_hand_value > current_hand_value:
                    print(f"****** You have a worse hand than the computer (you have {current_hand_value}, he has {current_computer_hand_value}). You LOOSE. ******")

            elif current_computer_hand_value > 22:
                print(f"****** 🎉 The computer's hand exceeded 22, you WIN 🎉. ******")

    else:
        print("Wrong input")
