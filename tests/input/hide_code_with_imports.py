quicksort = lambda a: qs1(a,0,len(a)-1)                               ; import a
qs1 = lambda a,lo,hi: qs2(a,lo,hi) if lo<hi else a                    ; import b
qs2 = lambda a,lo,hi: qs3(lo,hi,*qsp(a,lo,hi))                        ; import c
qs3 = lambda lo,hi,a,p: qs1(qs1(a,p+1,hi),lo,p-1)                     ; import d
qsp = lambda a,lo,hi: qsp1(a,lo,hi,a[hi],lo,lo)                       ; import e
qsp1 = lambda a,lo,hi,p,i,j: qsp2(a,lo,hi,p,i,j,j<hi)                 ; import f
qsp2 = lambda a,lo,hi,p,i,j,c: qspt(a,lo,hi,p,i,j,qsp3 if c else qsp7); import g
qspt = lambda a,lo,hi,p,i,j,n: n(a,lo,hi,p,i,j)                       ; import h
qsp3 = lambda a,lo,hi,p,i,j: qsp4(a,lo,hi,p,i,j,a[j]<p)               ; import i
qsp4 = lambda a,lo,hi,p,i,j,c: qspt(a,lo,hi,p,i,j,qsp5 if c else qsp6); import j
qsp5 = lambda a,lo,hi,p,i,j: qsp1(sw(a,i,j),lo,hi,p,i+1,j+1)          ; import k
qsp6 = lambda a,lo,hi,p,i,j: qsp1(a,lo,hi,p,i,j+1)                    ; import l
qsp7 = lambda a,lo,hi,p,i,j: (sw(a,i,hi), i)                          ; import m
sw = lambda a,i,j: sw1(enumerate(a),i,j,a[i],(-1,a[j]))               ; import n
sw1 = lambda a,i,j,ai,aj: sw2([aj if x[0]==i else x for x in a],j,ai) ; import o
sw2 = lambda a,j,ai: [ai if x[0]==j else x[1] for x in a]             ; import p
