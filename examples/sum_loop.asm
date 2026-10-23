; Suma 1 + 2 + ... + 10 en EAX.
        mov ecx, 10
        mov eax, 0
loop_start:
        add eax, ecx
        sub ecx, 1
        cmp ecx, 0
        jne loop_start
        hlt
