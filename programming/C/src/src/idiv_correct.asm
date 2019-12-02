; idiv_correct.asm 
;
; assemble:	nasm -f elf -g -F stabs idiv_correct.asm	
; link:		ld -o idiv_correct idiv_correct.o -melf_i386	

SECTION .data		; data section

SECTION .text		; code section
global _start		; make label available to linker 
_start:				; standard  nasm  entry point

	;;; Example 1 - zero extend eax
	mov		eax, 22
	mov		ebx, 4
	cdq
	idiv	ebx	

	;;; Example 2 - sign extend eax 
	mov		eax, -22
	mov		ebx, 4
	cdq
	idiv	ebx		
	nop
