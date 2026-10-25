; jmp: salto incondicional.
; No mira las flags ni las cambia: siempre salta.
; Observa: "mov eax, 99" nunca se ejecuta.
        mov eax, 1
        jmp fin
        mov eax, 99     ; nunca se ejecuta
fin:
        hlt             ; eax = 1
