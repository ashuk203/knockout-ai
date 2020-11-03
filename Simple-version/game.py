# Very simplified version with ASCII-based graphics
import random

class KnockoutLite:
    board_len = 4
    num_penguins = 2
    num_players = 2
    dead_flag = 'dead'

    def __init__(self):
        self.penguins = []

        for i in range(KnockoutLite.num_players * KnockoutLite.num_penguins):
            self.penguins.append([random.randrange(KnockoutLite.board_len), random.randrange(KnockoutLite.board_len)])


    def is_in_board(self, penguin):
        if penguin == KnockoutLite.dead_flag:
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
            if self.is_in_board(p):
                symbol = 'X' if p_idx // KnockoutLite.num_penguins == 0 else 'O'
                self.board[p[0]][p[1]] = check_and_update(self.board[p[0]][p[1]], symbol)

        for r in self.board:
            print(' '.join(r))

        # Print a new line
        print()


    @staticmethod
    def list_equals(l1, l2):
        if len(l1) == len(l2):
            for i in range(len(l1)):
                if l1[i] != l2[i]:
                    return False

            return True
        else:
            return False


    @staticmethod
    def two_collide(dir1, dir2):
        sum = dir1.copy()
        new_dir1 = dir1.copy()
        new_dir2 = dir2.copy()
        for dim in range(2):
            sum[dim] += dir2[dim]

        min_sum = min(abs(sum[0]), abs(sum[1]))
        for dim in range(2):
            if sum[dim] == min_sum:
                temp = new_dir1[dim]
                new_dir1[dim] = new_dir2[dim]
                new_dir2[dim] = temp

        return new_dir1, new_dir2

    @staticmethod
    def vec_diff(old_vec, new_vec):
        diff = []
        for i in range(len(old_vec)):
            diff.append(new_vec[dim] - old_vec[dim])
        return diff

    @staticmethod
    def vec_diff(v1, v2):
        sum = []
        for i in range(len(v1)):
            sum.append(v1[dim] + v2[dim])
        return sum

    @staticmethod
    # Multiple penguins meeting at a certain point
    def collide(dirs):
        pass


    def move_penguin(self, penguin_idx, direction):
        for dim in range(2):
            self.penguins[penguin_idx][dim] += direction[dim]
            if not self.is_in_board(self.penguins[penguin_idx]):
                self.penguins[penguin_idx] = KnockoutLite.dead_flag


    def execute_play(self, directions):
        pass

if __name__ == '__main__':
    game = KnockoutLite()
