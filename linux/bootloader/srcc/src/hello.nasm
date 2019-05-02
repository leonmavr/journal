SECTION .data
msg     db      'Hello World!', 0Ah   
msg_len equ		$-msg

 
SECTION .text
global  _start
 
_start:
 
    mov     edx, msg_len     ; number of bytes to write - one for each letter plus 0Ah (line feed character)
    mov     ecx, msg    ; move the memory address of our message string into ecx
    mov     ebx, 1      ; write to the STDOUT file
    mov     eax, 4      ; invoke SYS_WRITE (kernel opcode 4)
    int     80h
