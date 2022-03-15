import random

num_trials = 100
winnings = 0

cost = num_trials * 5

for item in range(0, num_trials):
    round_winning = 0
    for thing in range(0, 3):

        prize_num = random.randint(1, 100)

        if 0 < prize_num <= 5:
            round_winning += 5
        elif 5 < prize_num <= 25:
            round_winning += 2
        elif 25 < prize_num <= 65:
            round_winning += 1
    winnings += round_winning

        