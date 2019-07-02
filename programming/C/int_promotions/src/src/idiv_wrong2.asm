; idiv_wrong1.asm 
;
; assemble:	nasm -f elf -g -F stabs idiv_wrong1.asm	
; link:		ld -o idiv_wrong1 idiv_wrong1.o -melf_i386	

SECTION .data		; data section

SECTION .text		; code section
global _start		; make label available to linker 
_start:				; standard  nasm  entry point

	;;; Example 1 - zeroing edx before division
	xor		edx, edx 	; clear out edx 
	mov		eax, -21
	mov		ebx, 2
	idiv	ebx		; eax = edx:eax / ebx, edx = edx:eax % ebx
	nop

	;;; Example 2 - sign extend eax 
	mov edx, 0xffffffff
	mov eax, -21
	mov ebx, 2 		; do we get eax = 5 and edx = 1?
	idiv ebx
	nop
