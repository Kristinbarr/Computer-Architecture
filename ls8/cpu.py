"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # memory with 256 bytes
        self.reg = [0] * 8    # 8 general-purpose registers
        self.pc = 0           # program counter, pointing at current command
        self.sp = self.reg[7] # stack pointer, reg[7] reserved position
        
        self.branch_table = {
            
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#") # splits each line or comment into a list of strings
                    num = comment_split[0].strip() # removes spaces, ignores second index
                    if num == '': # ignore blank lines
                        continue
                    val = int(num, 2) # binary
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        print('RAM:', self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        '''Should accept an address and return the stored value in the ram'''
        return self.ram[address]
    
    def ram_write(self, address, value):
        '''Should accept an address and value and write the value to that place in ram'''
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        HLT = 0b00000001
        CAL = 0b01010000

        running = True

        while running:
            # instruction = self.ram[self.pc]
            instruction = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc+1)
            reg_b = self.ram_read(self.pc+2)

            if instruction == LDI: # save the value to reg
                # +1 is an register address, +2 is a value
                self.reg[reg_a] = reg_b
                self.pc += 3
            elif instruction == PRN: # print
                # get value from +1 (address at register)
                value = self.reg[reg_a]
                print(value)
                self.pc += 2
            elif instruction == MUL:
                self.alu('MUL', reg_a, reg_b)
                self.pc += 3
            # elif instruction == CAL:
            elif instruction == PUSH: # push value given to register
                # get value from register address
                value = self.reg[reg_a]
                # decrement stack pointer
                self.sp -= 1
                self.ram_write(self.sp, value)
                self.pc += 2
            elif instruction == POP: # return value given to register
                # get value from stack
                value = self.ram_read(self.sp)
                # set value to register address given
                self.reg[reg_a] = value
                # decrement stack pointer and add to program counter
                self.sp -= 1
                self.pc += 2
            elif instruction == HLT: # HLT - halt
                running = False
                self.pc += 1
            else:
                print('Unknown Instruction:', instruction)
                sys.exit(1)