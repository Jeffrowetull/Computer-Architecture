"""CPU functionality."""

import sys

AND = 0b10101000
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH= 0b01000101
POP = 0b01000110
CALL= 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110
MOD = 0b10100100
NOT = 0b01101001
OR  = 0b10101010
SHL = 0b10101100
SHR = 0b10101101
XOR = 0b10101011
AND = 0b10101000

SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.register = [0] * 8
        self.memory = [0] *256
        self.fl = 0

    def load(self,arg):
        """Load a program into memory."""

        address = 0
        try:
            with open(f'examples/{sys.argv[1]}.ls8') as f:
                for line in f:
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    val = int(num,2)
                    self.memory[address] = val
                    address += 1
                    
        except FileNotFoundError:
            print('File not found')
            sys.exit(2)

    def memory_read(self, mar):
        mdr = self.memory[mar]
        return mdr
    
    def memory_write(self, mdr, mar):
        self.memory[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == 'AND':
            self.register[reg_a] &= self.register[reg_b]
        elif op == 'MOD':
            self.register[reg_a] %= self.register[reg_b]
        elif op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
        elif op == 'NOT':
            self.register[reg_a] = ~self.register[reg_a]
        elif op == 'OR':
            self.register[reg_a] |= self.register[reg_b]
        elif op == 'SHL':
            self.register[reg_a] <<= self.register[reg_b]
        elif op == 'SHR':
            self.register[reg_a] >>= self.register[reg_b]
        elif op == 'SUB':
            self.register[reg_a] -= self.register[reg_b]
        elif op == 'CMP':
            # needs flags
            if self.register[reg_a] == self.register[reg_b]:
                self.fl = 0b00000001
            if self.register[reg_a] > self.register[reg_b]:
                self.fl = 0b00000010
            if self.register[reg_a] < self.register[reg_b]:
                self.fl = 0b00000100
        elif op == 'XOR':
            self.register[reg_a] ^= self.register[reg_b]
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
            self.memory_read(self.pc),
            self.memory_read(self.pc + 1),
            self.memory_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            opcode = self.memory[self.pc]
            operand_a = self.memory_read(self.pc + 1)
            operand_b = self.memory_read(self.pc + 2)
            if opcode == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif opcode == PRN:
                print(self.register[operand_a])
                self.pc += 2
            elif opcode == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif opcode == ADD:
                self.alu('ADD',operand_a,operand_b)
                self.pc += 3
            elif opcode == CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
            elif opcode == AND:
                self.alu('AND', operand_a, operand_b)
                self.pc += 3
            elif opcode == OR:
                self.alu('OR', operand_a, operand_b)
                self.pc += 3
            elif opcode == XOR:
                self.alu('XOR', operand_a, operand_b)
                self.pc += 3
            elif opcode == NOT:
                self.alu('NOT', operand_a, operand_b)
                self.pc += 2
            elif opcode == SHL:
                self.alu('SHL', operand_a, operand_b)
                self.pc += 3
            elif opcode == SHR:
                self.alu('SHR', operand_a, operand_b)
                self.pc += 3
            elif opcode == MOD:
                self.alu('MOD', operand_a, operand_b)
                self.pc += 3
            elif opcode == PUSH:
                reg = self.memory[self.pc + 1]
                val = self.register[reg]
                self.register[SP] -= 1
                self.memory[self.register[SP]] = val
                self.pc += 2
            elif opcode == POP:
                reg = self.memory[self.pc + 1]
                val = self.memory[self.register[SP]]
                # Copy the value from the address pointed to by SP to the given register.
                self.register[reg] = val
                # Increment SP.
                self.register[SP] += 1
                self.pc += 2
            elif opcode == CALL:
                self.register[SP] -= 1
                self.memory[self.register[SP]] = self.pc + 2
                reg = self.memory[self.pc + 1]
                self.pc = self.register[reg]
            elif opcode == RET:
                self.pc = self.memory[self.register[SP]]
                self.register[SP] +=1
            elif opcode == JMP:
                self.pc = self.register[operand_a]
            elif opcode == JEQ:
                if self.fl == 0b00000001:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2
            elif opcode == JNE:
                if self.fl != 0b00000001:

                    self.pc = self.register[operand_a]
                else:
                    self.pc +=2
            elif opcode == HLT:
                sys.exit(0)
            
            else:
                print(f"I did not understand that command: {opcode}")
                self.trace()
                sys.exit(1)
