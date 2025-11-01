# PyChip8
Another Python Chip8 emulator

Another atempt to test my low programming skills in writing an emulator. 
My first one was an I8080 arcade that runs Space Invaders. I finished it long ago (2010) for (now dead) J2ME and it really worked. Too bad I never released this J2ME build and source-code.
In 2022 I ported to python and improved it a lot, adding colors and sounds. You can find in my repository.

The main difference from this chip8 emulator is that now I wanted to write an emulator from scratch, only reading documentation. 
When I wrote the more complex I8080 emulator, I copied a lot of CPU instruction code from other sources without understanding how the instructions work.

I've also writen this emulator in 2022, but in that day, It had an unsolved collision bug in all games and I stopped working on it. 
Now in 2025 I checked the code and Eureka! I solved the collision bug and a lot of games seems to be working.
So I decided to publish. But be warned that my code is considerably worse than that of other programmers. To begin with, it's in a single file without any object-oriented practices.
The method of drawing sprites into screen is atrocious (but it works!). I'm thinking of improving it but i'm not interested in working in this emulator now.

Since ROMs are in the public domain I've included in the package. 
The keyboard controls are the default used in all windows chip8 emulators (1,2,3,4, Q, W, E, R and bellow).
