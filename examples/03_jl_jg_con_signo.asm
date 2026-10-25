; Comparación con signo: jg, jge, jl, jle miran SF, OF y ZF.
; Sirven cuando los números pueden ser negativos.
        mov eax, -3
        mov ebx, 2
        cmp eax, ebx    ; -3 - 2 = -5   ->  SF = 1, OF = 0
        jl  menor       ; salta si SF ≠ OF: -3 < 2
        hlt
menor:
        mov ecx, 1      ; ecx = 1: -3 es menor
        cmp ebx, eax    ; 2 - (-3) = 5  ->  SF = 0, OF = 0, ZF = 0
        jg  mayor       ; salta si ZF = 0 y SF = OF: 2 > -3
        hlt
mayor:
        mov edx, 1      ; edx = 1: 2 es mayor
        hlt
