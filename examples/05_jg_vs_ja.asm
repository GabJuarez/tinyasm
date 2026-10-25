; El mismo cmp, dos respuestas distintas.
; eax = -1 se guarda como 0xFFFFFFFF (mira las columnas del panel de registros):
;   con signo:  -1 > 1          es falso  ->  jg no salta
;   sin signo:  4294967295 > 1  es cierto ->  ja salta
        mov eax, -1
        mov ebx, 1
        cmp eax, ebx    ; CF = 0, ZF = 0, SF = 1, OF = 0
        jg  mayor_con_signo
        ja  mayor_sin_signo
        hlt
mayor_con_signo:
        mov ecx, 1      ; no se llega aquí
        hlt
mayor_sin_signo:
        mov ecx, 2      ; ecx = 2: sólo ja saltó
        hlt
