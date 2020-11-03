# Very simplified version with ASCII-based graphics
import random

class KnockoutLite:
    board_len = 3
    num_penguins = 1
    num_players = 2

    dead_flag = ['dead']
    is_dead = lambda p : p == ['dead']

    def __init__(self):
        self.penguins = []
        self.move_number = 1

        for i in range(KnockoutLite.num_players * KnockoutLite.num_penguins):
            self.penguins.append([random.randrange(KnockoutLite.board_len), random.randrange(KnockoutLite.board_len)])

    def display_game_results(self):
        if any(map(KnockoutLite.is_dead, self.penguins)):
            if all(map(KnockoutLite.is_dead, self.penguins)):
                print("It's a tie! (both players died)")
            elif KnockoutLite.is_dead(self.penguins[0]):
                print("Player 2 wins.")
            else:
                print("Player 1 wins.")
        else:
            print("Game is still running...")

    def is_in_board(self, penguin_idx):
        penguin = self.penguins[penguin_idx]
        if KnockoutLite.is_dead(penguin):
            return False

        in_board = True
        for dim in range(2):
            in_board = in_board and penguin[dim] >= 0 and penguin[dim] < KnockoutLite.board_len
        return in_board


    def draw_board(self):
        self.board = [['-' for r in range(KnockoutLite.board_len)] for c in range(KnockoutLite.board_len)]

        check_and_update = lambda curr, new : curr + new if curr != '-' else new

        for p_idx in range(len(self.penguins)):
            p = self.penguins[p_idx]
            if self.is_in_board(p_idx):
                symbol = 'X' if p_idx // KnockoutLite.num_penguins == 0 else 'O'
                self.board[p[0]][p[1]] = check_and_update(self.board[p[0]][p[1]], symbol)

        for r in self.board:
            print(' '.join(r))

        # Print a new line
        print()


    @staticmethod
    def swap_elems(lst, i, j):
        temp = lst[i]
        lst[i] = lst[j]
        lst[j] = temp


    def move_penguin(self, penguin_idx, direction):
        for dim in range(2):
            self.penguins[penguin_idx][dim] += direction[dim]


    # Returns whether game can continue after executed play
    def execute_play(self, directions, powers):
        print("-"*8 + " Executing play number " + str(self.move_number) + " " + "-"*8)
        p1_prev = self.penguins[0].copy()
        p2_prev = self.penguins[1].copy()
        player_is_out = False

        while max(powers) > 0:
            for p_idx in range(KnockoutLite.num_players):
                if powers[p_idx] > 0 and not KnockoutLite.is_dead(self.penguins[p_idx]):
                    self.move_penguin(p_idx, directions[p_idx])
                    powers[p_idx] -= 1
                    if not self.is_in_board(p_idx):
                        self.penguins[p_idx] = KnockoutLite.dead_flag
                        player_is_out = True

            # Emulate collisions by simply switching the velocities on impact
            # (physically accurate since momentum is conserved)
            if not player_is_out and (self.penguins[0] == self.penguins[1] or (self.penguins[0] == p2_prev and self.penguins[1] == p1_prev)):
                KnockoutLite.swap_elems(directions, 0, 1)
                KnockoutLite.swap_elems(powers, 0, 1)
                if self.penguins[0] != self.penguins[1]:
                    KnockoutLite.swap_elems(self.penguins, 0, 1)
                    powers = list(map(lambda x: x + 1, powers))
            elif all(map(KnockoutLite.is_dead, self.penguins)):
                return False

            self.draw_board()
            p1_prev = self.penguins[0].copy()
            p2_prev = self.penguins[1].copy()

        self.move_number += 1
        return not player_is_out


# Running the game
def update_game_params(p_inps, directions, powers):
    directions.append([-int(p_inps[1]), int(p_inps[0])])
    powers.append(int(p_inps[2]))


if __name__ == '__main__':
    game = KnockoutLite()

    run_game = True
    print("Welcome, Player 1 is 'X', Player 2 is 'O'. The positive x and y directions are right and up, respectively. Each input line consists of 3 ** integers ** seperated by spaces. Each direction dimension's range is [-1, 1]. The power must be in the range [1, 3].")
    game.draw_board()

    while run_game:
        directions = []
        powers = []

        print("Enter Player 1 direction and power: dirx diry pow ")
        p1_inps = input().split(" ")

        print("Enter Player 2 direction and power: dirx diry pow")
        p2_inps = input().split(" ")

        update_game_params(p1_inps, directions, powers)
        update_game_params(p2_inps, directions, powers)

        run_game = game.execute_play(directions, powers)

    game.display_game_results()
