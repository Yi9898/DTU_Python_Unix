#!/bin/bash
paste ex1.acc ex1.dat > ex1.tot
echo "19. The head of the output is: "
head ex1.tot
 
cut -f1,5 ex1.tot > ex1.res
echo "20. The head of the output is: "
head ex1.res

echo "21. The tail of the output is: "
sort -n -k2 ex1.res | tail -3

echo "22. The number of lines containing a GeneBank accession number is: "
grep -c "^>" orphans.sp

echo "23. The number of human genes with Swissprot ID is: "
grep -c "HUMAN (" orphans.sp
echo "23. The number of hypothetical human genes is: "
grep "HUMAN (" orphans.sp | grep "HYPOTHETICAL" | wc -l

echo "24. The number of rat genes is: "
grep -c MOUSE orphans.sp
echo "24. The number of precursor rat genes is: "
grep "MOUSE" orphans.sp | grep "PRECURSOR" | wc -l
