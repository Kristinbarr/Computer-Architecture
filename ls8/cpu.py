"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8 # 8 general-purpose registers
        self.ram = [0] * 256 # memory with 256 bytes

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # LDI: load "immediate", store a value in a register, or "set this register to this value".
        # PRN: a pseudo-instruction that prints the numeric value stored in a register.
        # HLT: halt the CPU and exit the emulator.

        # For now, we've just hardcoded a program:
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
            with open(filename) as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split("#")
                    # Strip out whitespace
                    num = comment_split[0].strip()
                    # Ignore blank lines
                    if num == '':
                        continue
                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def ram_read(self, mar):
        """Should accept the address to read and return the value stored in the ram."""
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        """Should accept a value to write, and the address to write it to.
        MAR - Memory Address Register, MDR - Memory Data Register"""
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU. PC - Program Counter, IR - Instruction Register"""
        running = True

        while running:
            ir = self.ram[self.pc]
            # if inst code starts with 01XXXXXX, it has 1 operand
            if ir > 64:
                operand_a = self.ram_read(self.pc+1)
                self.pc += 1
            # if inst code starts with 10XXXXXX, it has 2 operands
            if ir > 128:
                operand_b = self.ram_read(self.pc+1)
                self.pc += 1

            if ir == 0b10000010: # LDI
                self.reg[operand_a] = operand_b
            elif ir == 0b01000111: # PRN
                print(self.reg[operand_a])
            elif ir == 0b10100010: # MUL R0,R1
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
            elif ir == 0b00000001: # HLT
                exit()
            self.pc += 1