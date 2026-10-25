; CF, OF y SF también los encienden add y sub, no sólo cmp.
;   CF: el resultado sin signo no cabe en 32 bits.
;   OF: el resultado con signo no cabe (pasa de positivo a negativo o al revés).
;   SF: el bit 31 del resultado es 1 (negativo si se lee con signo).
        mov eax, 0xFFFFFFFF
        add eax, 1      ; sin signo no cabe: eax = 0, CF = 1, ZF = 1
        jc  hubo_carry  ; salta si CF = 1
        hlt
hubo_carry:
        mov eax, 0x7FFFFFFF ; el positivo más grande con signo
        add eax, 1      ; con signo da la vuelta: OF = 1, SF = 1
        jo  hubo_overflow   ; salta si OF = 1
        hlt
hubo_overflow:
        mov ecx, 1      ; mov no cambia las flags: SF sigue en 1
        js  negativo    ; salta si SF = 1
        hlt
negativo:
        mov edx, 1      ; edx = 1: llegó hasta el final
        hlt
