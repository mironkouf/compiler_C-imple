# compiler_C-imple
In this project we have a compiler for the visual programming language C-imple. We input a program in .ci and the output is a program in assembly (.asm) for the RISC-V. 
The first part is the lexical analysis, in which we read character-character the file.
The second part is the syntax analysis, in which we check for errors in the syntax of the programming language given.
The third part is the intermediate code generation, in which we create quads to help the code generator (.c and .int).
The fourth part is the symbol table management, in which we create the scopes to be able to understand the visibility of our variables (.symb).
The fifth part is the code generator, in which we create the assembly code for the RISC-V (.asm). We also give some examples of programs in .ci. 
