# Prepping Training data Patches
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

# Prepping Training data Full images
mkdir labeled_Full_images

# cp only " w1 " (nuclei) labeled images from rand 200,500, 1000 files sets
cp `cat ../cell_locations_out/Cell_locations_200.csv| tr ',' '\t'| cut -f 1 | grep "w1"| sed -E 's/(.+)/\1.TIFF/'` ../labeled_Full_images
cp `cat ../cell_locations_out/Cell_locations_500.csv| tr ',' '\t'| cut -f 1 | grep "w1"| sed -E 's/(.+)/\1.TIFF/'` ../labeled_Full_images
cp `cat ../cell_locations_out/Cell_locations_1000.csv| tr ',' '\t'| cut -f 1 | grep "w1"| sed -E 's/(.+)/\1.TIF/'` ../labeled_Full_images

# convert to jpg
convert *.tiff -set filename: "%t" %[filename:].jpg

# disperse into Validation, Test and Prediction files sets
mv `ls -1 | shuf | head -n 28` ../Test/
mv `ls -1 | shuf | head -n 28` ../Validation/

# prep class folders for each cell count GroundTruth
mkdir `ls -1 | tr "_" '\t' | cut -f 3 | sort | uniq | grep -Eo "[0-9]+"`
