.386
.MODEL FLAT
.DATA
X DD ?
Y DD ?
adr DD ?
DVA DD 2.0

.CODE
_solution PROC
PUSH EBP
MOV EBP, ESP

MOV EAX, [EBP]+8
MOV X, EAX

MOV EAX, [EBP]+12
MOV adr, EAX

FINIT; приводим сопроцессор в начальное состояние
FLD X; st(0) = x
FPTAN; ST(0) = 1; st(1) = tg(x)
FSTP ST; st(0) = tg(x)
FLD DVA; st(0) = 2; st(1) = tg(x)
FDIVP; st(0) = tg(x)/2
FSTP Y; st(0) = 0 ;в Y результат

MOV ECX, adr
MOV EDX, Y
MOV [ECX], EDX
POP EBP
RET

POP EBP
RET
_solution ENDP
END
