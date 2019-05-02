; Skeleton of a Nasm program
; To compile:
; nasm -f elf -g -F dwarf empty.nasm -o empty.o
; To link:
; ld -m elf_i386 empty.o -o empty

SECTION .data

SECTION .text
global  _start
 
_start:
    mov     ebx, 0      ; return 0 status on exit - 'No Errors'
    mov     eax, 1      ; invoke SYS_EXIT (kernel opcode 1)
    int     80h
