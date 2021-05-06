from pwn import *


target = process('./labyrinth')


class Node:
    def __init__(self, left=None, right=None, val=None):
        self.left, self.right, self.val = left, right, val


Graph = {
    'a': Node('c','g',0xe3),
    'b': Node('e','d',0x1f9),
    'c': Node('d','g',0x468),
    'd': Node('i','d',0x213),
    'e': Node('f','h',0x121),
    'f': Node('a','f',0x3a9),
    'g': Node('j','a',0x19a),
    'h': Node('a','j',0x13a),
    'i': Node('j','b',0x362),
    'j': Node('j','d',0x2c6)
    }


goal = 0x257B


def traverse(node = 'a', total = 0, path = ""):
    curr_sum = total + Graph[node].val

    if curr_sum <= goal:
        l, l_sum = traverse(Graph[node].left, curr_sum, path + 'L')
        r, r_sum = traverse(Graph[node].right, curr_sum, path + 'R')
        return (l, l_sum) if l_sum == goal else (r, r_sum)
    return path, total



def solve(target):
    target.readline()   
    solve = traverse()
    print(solve)
    target.sendline(solve[0])
    print(target.recvline())
    return target.recvline()



def main():
    print(solve(target))

if __name__ == '__main__':
    main()

