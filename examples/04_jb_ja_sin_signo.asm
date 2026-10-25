; Comparación sin signo: ja, jae, jb, jbe miran CF y ZF.
; CF se enciende cuando a < b sin signo: la resta "pide prestado".
        mov eax, 3
        mov ebx, 10
        cmp eax, ebx    ; 3 - 10 necesita préstamo  ->  CF = 1
        jb  abajo       ; salta si CF = 1: 3 < 10
        hlt
abajo:
        mov ecx, 1      ; ecx = 1: 3 está abajo de 10
        cmp ebx, eax    ; 10 - 3 = 7  ->  CF = 0, ZF = 0
        ja  arriba      ; salta si CF = 0 y ZF = 0: 10 > 3
        hlt
arriba:
        mov edx, 1      ; edx = 1: 10 está arriba de 3
        hlt
