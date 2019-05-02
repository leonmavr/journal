SECTION .data
msg     db      'in the loop!', 0Ah   
        times 32-$+msg db '.'
msg_len equ      $-msg

 
SECTION .text
global  _start
 
_start:
    ; number of bytes to write - one for each letter plus 0Ah (line feed character)
    mov     edx, msg_len
    mov     ecx, msg    ; move the memory address of our message string into ecx
    mov     ebx, 1      ; write to the STDOUT file
    mov     eax, 4      ; invoke SYS_WRITE (kernel opcode 4)
    int     80h         ; print interrupt - it overwrites the registers
    jmp     $-22        ; jump right below _start label - 22 = int + 4*mov	
