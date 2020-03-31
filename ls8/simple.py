# simple example of ls8

import sys

# define operation (OP) codes
PRINT_BEEJ = 1
HALT       = 2
PRINT_NUM  = 3
SAVE       = 4 # save a value to a register
PRINT_REG  = 5 # print a value from a register
ADD        = 6 # regA += regB

# RAM - need a place to store
# memory is a long single dimentional array of 1s and 0s
# think about these commands as bytes(00000001)
memory = [
    PRINT_BEEJ,
    SAVE,
    65,
    2,
    SAVE,
    20,
    3,
    ADD,
    2,
    3,
    PRINT_REG,
    2,
    HALT
]

# register - fast group of data storage
# registers are baked into hardware, fast and small, holds one word
register = [0] * 8

# use a program counter (PC) - a pointer for which instruction to run
pc = 0

# flag to show our program still running
running = True

# Processor -> REPL
while running:
    command = memory[pc]

    # each command is a spot in our CPU
    if command == PRINT_BEEJ:
        print('Beej!')
        pc += 1

    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
        # get argument of the next index in memory
        num = memory[pc + 1]
        print(num)
        pc += 3

    elif command == PRINT_REG:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2

    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3

    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3

    else:
        print(f'Unkown Instruction: {command}')
        sys.exit(1)
