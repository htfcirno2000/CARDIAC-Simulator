class Cardiac:
    def __init__(self, inputCards):
        self.mem = [0]*100 # 100 cells of memory
        self.acc = 0  # accumulator
        self.ir  = 0  # instruction register
        self.pc  = 0  # program counter
        self.halted = False
        self.mem[0] = 1 # starting code to load stuff
        self.inputCards = inputCards

    def fetch(self):  # fetch instruction from memory
        return self.mem[self.pc]
    
    def getOpcode(self): # get opcode of instruction
        return (self.ir - self.ir % 100) // 100

    def getAddress(self): # get address of instruction
        return self.ir % 100

    def getLR(self): # L and R for SFT instruction
        L = ((self.ir % 100) - ((self.ir % 100) % 10)) // 10 
        R = (self.ir % 100) % 10 
        return L,R

    def getCard(self): # get "card" which is really a 3 digit integer
        if self.inputCards:
            return self.inputCards.pop(0)
        else:
            return 0
        
    def step(self): # cpu step       
        self.ir = self.fetch()         # fetch instruction
        opcode = self.getOpcode()      # grab opcode from instruction
        address = self.getAddress()    # grab address from instruction
        self.pc = (self.pc + 1) % 100  # increment program counter
        
        match opcode:
            case 0: # inp
                self.mem[address] = self.getCard()
            case 1: # cla
                self.acc = 0
                self.acc += self.mem[address]
            case 2: # add
                self.acc += self.mem[address]
            case 3: # tac
                if self.acc < 0:
                    self.pc = address
            case 4: # sft
                l,r = self.getLR
                self.acc = (self.acc * 10^l) / 10^r
            case 5: # out
                print(self.mem[address])
            case 6: # sto
                self.mem[address] = self.acc
            case 7: # sub
                self.acc -= self.mem[address]
            case 8: # jmp
                self.mem[99] = self.pc + 800
                self.pc = address
            case 9: # HRS
                self.halted = True
    def coreDump(self):
        for index, cell in enumerate(self.mem):
            if index % 10 == 0:
                print()
            print(f'{cell:03d} ', end='')
            
            
cardpile = []        
with open("towers-of-hanoi.txt","r") as file:
    for line in file.readlines():
        cardpile.append(int(line.strip()))

CPU = Cardiac(cardpile)

while not CPU.halted:
    CPU.step()

CPU.coreDump()
