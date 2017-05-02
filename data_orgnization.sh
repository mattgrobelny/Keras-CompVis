# Prepping Training data
# Copy patches
cp `ls -1 | grep -E "_CX_0"`  ../Working_Sets_Patches/Training/0/
cp `ls -1 | grep -E "_CX_1"`  ../Working_Sets_Patches/Training/1/
cp `ls -1 | head -n 4000 | grep -E "_CX_1"`  ../Working_Sets_Patches/Training/1/
cp `ls -1 | tail -n 5000 | grep -E "_CX_1"`  ../Working_Sets_Patches/Training/1/

# Move random 20% from Training 0 or 1 into test and Validation 
mv `ls -1 | shuf | head -n 1339` ../../Test/1/
mv `ls -1 | shuf | head -n 1339` ../../Validation/1/
mv `ls -1 | shuf | head -n 487` ../../Validation/0/
mv `ls -1 | shuf | head -n 487` ../../Test/0/
