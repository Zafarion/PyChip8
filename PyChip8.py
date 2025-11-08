import pygame
import sys
import os
import winsound
from random import seed
from random import randint
import time as t

pygame.init()
seed(1)

header = [(0xF0),(0x90),(0x90),(0x90),(0xF0),
          (0x20),(0x60),(0x20),(0x20),(0x70),
          (0xF0),(0x10),(0xF0),(0x80),(0xF0),
          (0xF0),(0x10),(0xF0),(0x10),(0xF0),
          (0x90),(0x90),(0xF0),(0x10),(0x10),
          (0xF0),(0x80),(0xF0),(0x10),(0xF0),
          (0xF0),(0x80),(0xF0),(0x90),(0xF0),
          (0xF0),(0x10),(0x20),(0x40),(0x40),
          (0xF0),(0x90),(0xF0),(0x90),(0xF0),
          (0xF0),(0x90),(0xF0),(0x10),(0xF0),
          (0xF0),(0x90),(0xF0),(0x90),(0x90),
          (0xE0),(0x90),(0xE0),(0x90),(0xE0),
          (0xF0),(0x80),(0x80),(0x80),(0xF0),
          (0xE0),(0x90),(0x90),(0x90),(0xE0),
          (0xF0),(0x80),(0xF0),(0x80),(0xF0),
          (0xF0),(0x80),(0xF0),(0x80),(0x80)]

keys = (pygame.K_x, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_z, pygame.K_c, pygame.K_4, pygame.K_r, pygame.K_f, pygame.K_v)

#Registers
V = [0] * 16
I = 0
PC = 0x200
DT = 0
ST = 0
SP = 0
Stack = [0] * 16

#Control variables
cycles = 0
frame = 0
crashed = False

black = (0, 0, 0)
blue = (83, 83, 241)
white = (255, 255, 255)
pixelColor = (black, blue)
screen = pygame.display.set_mode((64 * 16, 32 * 16))
native_screen = pygame.Surface((64, 32))
pygame.display.set_caption("Another Python Chip8 emulator")
font = pygame.font.SysFont("Retro.ttf", 20)
screen.blit(font.render('Click the ROM filename to load (max 67 files in the dir):', True, blue), (0, 0))

dir = os.listdir()
list_x_axis = []
list_y_axis = []
x_axis = 0
y_axis = 15

for l in range(len(dir)):
    text = font.render(dir[l], True, white)
    list_x_axis.append(x_axis)
    list_y_axis.append(y_axis)
    screen.blit(text, (x_axis, y_axis))
    y_axis += 15
    if l == 32:
        x_axis = 512
        y_axis = 0

pygame.display.flip()

click = False
while not click:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        for l in range(len(dir)):
            if (mouse[0] <= list_x_axis[l] + 512) and (mouse[1] >= list_y_axis[l] and mouse[1] < list_y_axis[l + 1]):
                ram = bytearray(open(dir[l], "rb").read()) #Loading ROM into RAM
                click = True
                break

#Inserting header into RAM and extending it
for a in range(0x200 - len(header)):
    ram.insert(0, 0)
ram = bytearray(header) + ram
ram.extend([0] * (0x1000 - len(ram)))
        
def natural(number):
    if number < 0: return 0
    else: return number

#Main Loop
while not crashed:
    time = t.time()
     
    match ram[PC] >> 4:
        case 0x0:
            match ram[PC + 1]:
                case 0xE0: # CLS
                    native_screen.fill(black)
                    PC += 2
                    #print('CLS')
                case 0xEE: # RET
                    SP -= 1
                    PC = Stack[SP]
                    #print('RET', PC)
                    PC += 2
                case _:
                    #PC = ((ram[PC] & 0x0F) << 8) + (ram[PC + 1]) # SYS addr
                    #print('SYS', PC)

                    print ('Undefined Opcode: 0' + str(hex(ram[PC + 1])))
                    pygame.quit()
                    sys.exit()
                    
        case 0x1: # JP addr
            PC = ((ram[PC] & 0x0F) << 8) + ram[PC + 1]
        case 0x2: # CALL addr
            Stack[SP] = PC
            SP += 1
            PC = ((ram[PC] & 0x0F) << 8) + ram[PC + 1]
        case 0x3: # SE Vx, byte
            if V[ram[PC] & 0x0F] == ram[PC + 1]:
                PC += 2
            PC += 2
        case 0x4: # SNE Vx, byte
            if V[ram[PC] & 0x0F] != ram[PC + 1]:
                PC += 2
            PC += 2
        case 0x5: # SE Vx, Vy
            if V[ram[PC] & 0x0F] == V[ram[PC + 1] >> 4]:
                PC += 2
            PC += 2
        case 0x6: # LD Vx, byte
            V[ram[PC] & 0x0F] = ram[PC + 1]
            PC += 2
        case 0x7: # ADD Vx, byte
            V[ram[PC] & 0x0F] = (V[ram[PC] & 0x0F] + ram[PC + 1]) & 0xFF
            PC += 2
        case 0x8:
            match ram[PC + 1] & 0x0F: 
                case 0x0: # LD Vx, Vy
                    V[ram[PC] & 0x0F] = V[ram[PC + 1] >> 4]
                    PC += 2
                case 0x1: #OR Vx, Vy
                    V[ram[PC] & 0x0F] |= V[ram[PC + 1] >> 4]
                    V[0xF] = 0
                    PC += 2
                case 0x2: #AND Vx, Vy
                    V[ram[PC] & 0x0F] &= V[ram[PC + 1] >> 4]
                    V[0xF] = 0
                    PC += 2
                case 0x3: #XOR Vx, Vy
                    V[ram[PC] & 0x0F] ^= V[ram[PC + 1] >> 4]
                    V[0xF] = 0
                    PC += 2
                case 0x4: #ADD Vx, Vy
                    temp = V[ram[PC] & 0x0F]
                    V[ram[PC] & 0x0F] = (V[ram[PC] & 0x0F] + V[ram[PC + 1] >> 4]) & 0xFF
                    if temp + V[ram[PC + 1] >> 4] > 255: V[0xF] = 1
                    else: V[0xF] = 0
                    PC += 2
                case 0x5: #SUB Vx, Vy
                    temp = V[ram[PC] & 0x0F]
                    V[ram[PC] & 0x0F] = (V[ram[PC] & 0x0F] - V[ram[PC + 1] >> 4]) & 0xFF
                    if temp >= V[ram[PC + 1] >> 4]: V[0xF] = 1
                    else: V[0xF] = 0
                    PC += 2
                case 0x6: #SHR Vx {, Vy}
                    temp = V[ram[PC] & 0x0F]
                    #V[ram[PC] & 0x0F] = V[ram[PC] & 0x0F] >> 1
                    V[ram[PC] & 0x0F] = V[ram[PC + 1] >> 4] >> 1
                    if temp & 1: V[0xF] = 1
                    else: V[0xF] = 0
                    PC += 2
                case 0x7: #SUBN Vx, Vy
                    temp = V[ram[PC] & 0x0F]
                    V[ram[PC] & 0x0F] = (V[ram[PC + 1] >> 4] - V[ram[PC] & 0x0F]) & 0xFF
                    if V[ram[PC + 1] >> 4] >= temp: V[0xF] = 1
                    else: V[0xF] = 0
                    PC += 2
                case 0xE: #SHL Vx {, Vy}
                    temp = V[ram[PC] & 0x0F]
                    #V[ram[PC] & 0x0F] = (V[ram[PC] & 0x0F] << 1) & 0xFF
                    V[ram[PC] & 0x0F] = (V[ram[PC + 1] >> 4] << 1) & 0xFF
                    if (temp >> 7): V[0xF] = 1
                    else: V[0xF] = 0
                    PC += 2
                case _:
                    print ('Undefined Opcode: 8' + str(hex(ram[PC + 1])))
                    pygame.quit()
                    sys.exit()
                    
        case 0x9: #SNE Vx, Vy
            if V[ram[PC] & 0x0F] != V[ram[PC + 1] >> 4]: PC += 2
            PC += 2
        case 0xA: #LD I, addr
            I = ((ram[PC] & 0x0F) << 8) + ram[PC + 1]
            PC += 2
        case 0xB: #JP V0, addr
            PC = ((ram[PC] & 0x0F) << 8) + ram[PC + 1] + V[0]
        case 0xC: #RND Vx, byte
            V[ram[PC] & 0x0F] = randint(0, 255) & ram[PC + 1]
            PC += 2
        case 0xD: #DRW Vx, Vy, nibble
            x = (V[ram[PC] & 0x0F]) & 0x3F
            y = (V[ram[PC + 1] >> 4]) & 0x1F
            n = ram[PC + 1] & 0x0F
            
            V[0xF] = 0

            for row in range(n):
                for column in range(8):
                    if (x + column) < 64 and (y + row) < 32:
                        oldPixel = pixelColor.index(native_screen.get_at(((x + column), (y + row))))
                        newPixel = ram[I + row] >> (7 - column) & 1
                        if oldPixel and newPixel: V[0xF] = 1
                        native_screen.set_at(((x + column), (y + row)), pixelColor[oldPixel ^ newPixel])
                    #else: print('Screen Overflow:', x + column, y + row)
                        
            pygame.transform.scale(native_screen, screen.get_size(), screen)
                        
            PC += 2
        case 0xE:
            match ram[PC + 1]:
                case 0x9E: #SKP Vx
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    keycode = pygame.key.get_pressed()
                    if keycode[keys[V[ram[PC] & 0x0F]]]:
                        PC += 2
                    PC += 2
                case 0xA1: #SKNP Vx
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    keycode = pygame.key.get_pressed()
                    if not keycode[keys[V[ram[PC] & 0x0F]]]:
                        PC += 2
                    PC += 2
                case _:
                    print ('Undefined Opcode: E' + str(hex(ram[PC + 1])))
                    pygame.quit()
                    sys.exit()
        case 0xF:
            match ram[PC + 1]:
                case 0x07: #LD Vx, DT
                    V[ram[PC] & 0x0F] = DT
                    PC += 2
                case 0x0A: #LD Vx, K
                    pygame.display.flip()
                    DT = 0
                    ST = 0
                    click = False
                    while not click:
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            keycode = pygame.key.get_pressed()
                            for k in range(len(keys)):
                                if keycode[keys[k]]:
                                    V[ram[PC] & 0x0F] = k
                                    click = True
                                    break
                    PC += 2
                case 0x15: #LD DT, Vx
                    DT = V[ram[PC] & 0x0F]
                    PC += 2
                case 0x18: #LD ST, Vx
                    ST = V[ram[PC] & 0x0F]
                    PC += 2
                case 0x1E: #ADD I, Vx
                    I += V[ram[PC] & 0x0F]
                    if I > 0xFFF: V[0xF] == 1
                    else: V[0xF] == 0
                    PC += 2
                case 0x29: #LD F, Vx
                    I = V[ram[PC] & 0x0F] * 5
                    PC += 2
                case 0x33: #LD B, Vx
                    ram[I] = (V[ram[PC] & 0x0F] // 100) % 10
                    ram[I + 1] = (V[ram[PC] & 0x0F] // 10) % 10
                    ram[I + 2] = (V[ram[PC] & 0x0F] // 1) % 10
                    PC += 2
                case 0x55: #LD [I], Vx
                    for i in range((ram[PC] & 0x0F) + 1):
                        #ram[I + i] = V[i]
                        ram[I] = V[i]
                        I += 1
                    PC += 2
                case 0x65: #LD Vx, [I]
                    for i in range((ram[PC] & 0x0F) + 1):
                        #V[i] = ram[I + i]
                        V[i] = ram[I]
                        I += 1
                    PC += 2
                case _:
                    print ('Undefined Opcode: F' + str(hex(ram[PC + 1])))
                    pygame.quit()
                    sys.exit()
        case _:
            print ('Undefined Opcode:', hex(ram[PC + 1]))
            pygame.quit()
            sys.exit()

    cycles += 1
    frame += t.time() - time
    if cycles == 8:
        t.sleep(natural(0.0166666666666667 - frame))
        pygame.display.flip()
        if DT > 0: DT -= 1
        if ST > 0:
            winsound.Beep(2500, 1)
            ST -= 1
        cycles = 0
        frame = 0

