# PyChip8
Chip8 emulator

Another atempt to test my low programming skills in writing an emulator. 
My first one was an I8080 arcade that runs Space Invaders. I finished it long ago (2010) for (now dead) J2ME and it really worked. Too bad I never released this J2ME build and source-code.
In 2022 I ported to python and improved it a lot, adding colors and sounds. You can find in my repository.

The main difference from this chip8 emulator is that now I wanted to write an emulator from scratch, only reading documentation. 
When I wrote the more complex I8080 emulator, I copied a lot of CPU instruction code from other sources without understanding how the instructions work.

I've writen this emulator in 2022, but in that day, It had an unsolved collision bug in all games and I stopped working on it. 
But now in 2025 I checked the code and Eureka! I solved the collision bug and some games started to run properly.
So I decided to publish. But be warned that my code may be worse than that of other programmers. To begin with, it's in a single file without any object-oriented practices.
I've also doing all the screen drawing directly in a pygame surface (no separate framebuffer) and using the surface direcly to check collisions, but it's seems to be working flawlessly.

After that, I started messing with it again and I worked to pass on all Timendus test ROMs. Now I think most - if not all - games are running perfecly.
BUT A WARNING: this emulator is based on the first chip8 interpreters, so many newer games - for example: HIDDEN, INVADERS - don't run properly.
For these games, use the SUPER CHIP emulator in my repository. That is an upgrade of chip8 and is backwards compatible with chip8 games. 
It seems like that most newer games - even if created for chip8 - were developed with SUPER CHIP in mind and are using the modified SUPER CHIP instructions.

Since ROMs are in the public domain I've included in the package.

INSTRUCTIONS:

To play, put your Chip8 ROMs in the same directory of the executable.
The keyboard controls are the default used in all windows chip8 emulators (1, 2, 3, 4, Q, W, E, R and bellow).

![](https://github.com/Zafarion/PyChip8/blob/main/b539b6f3-6481-4a7e-85d5-25f5491928bf.jpeg)
![](https://github.com/Zafarion/PyChip8/blob/main/cfb9804c-be26-4f3a-8165-292dba4088e0.jpeg)
![](https://github.com/Zafarion/PyChip8/blob/main/01c74cf3-0480-4deb-969a-1a19eac1f2b6.jpeg)
![](https://github.com/Zafarion/PyChip8/blob/main/8063c452-d614-4947-b53d-632271f1e551.jpeg)
