; imul_only.asm  
;
; assemble:	nasm -f elf -g -F stabs imul_only.asm	
; link:		ld -o imul_only imul_only.o -melf_i386	

SECTION .data		; data section
	; dd = double word (32 bits)
	val1:	dd 10, 10 			; 10 = line end
	val2:	dd -10, 10 			; 10 = line end

SECTION .text		; code section
global _start		; make label available to linker 
_start:				; standard  nasm  entry point
	;;; Example 1 - one operand
	mov		ecx, 2
	mov		eax, [val1]
	; edx:eax = eax * ecx 
	imul	ecx		; stores the 64-bit result in (high:low) EDX:EAX

	;;; Example 2 - one operand
	xor		eax, eax ; Clear eax register
	mov		ecx, 2
	mov		eax, [val2]
	; edx:eax = eax * ecx 
	imul	ecx		; result edx:eax < 0 so sign extended 

	;;; Example 3 - two operands
	mov		eax, 2 ; Clear eax register
	; eax = eax * [val2] 
	imul	eax, [val2]

	;;; Example 4 - three operands
	; imul r, r/m32, const_value
	; eax = [val2] * 3
	imul	eax, [val2], 3
	nop
