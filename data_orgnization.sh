# Prepping Training data

cp `ls -1 | grep -E "_CX_0"`  ../Working_Sets_Patches/Training/0/
cp `ls -1 | grep -E "_CX_1"`  ../Working_Sets_Patches/Training/1/
cp `ls -1 | head -n 4000 | grep -E "_CX_1"`  ../Working_Sets_Patches/Training/1/
cp `ls -1 | tail -n 5000 | grep -E "_CX_1"`  ../Working_Sets_Patches/Training/1/
