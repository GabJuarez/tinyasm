; cmp a, b calcula a - b sin guardar el resultado: sólo cambia las flags.
; je / jne miran ZF, que se enciende cuando la resta da 0 (a == b).
        mov eax, 7
        mov ebx, 7
        cmp eax, ebx    ; 7 - 7 = 0   ->  ZF = 1
        je  iguales     ; salta si ZF = 1
        hlt
iguales:
        mov ecx, 1      ; ecx = 1: eran iguales
        cmp eax, 5      ; 7 - 5 = 2   ->  ZF = 0
        jne distintos   ; salta si ZF = 0
        hlt
distintos:
        mov edx, 1      ; edx = 1: 7 y 5 son distintos
        hlt
