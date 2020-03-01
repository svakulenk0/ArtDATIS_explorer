
* find file in subfolders:
```
find . -name "foo*"
```

* remove folders from list:

#!/bin/bash

for folder in JP2 JPG TIF
do
  for subfolder in 2153 2154 2156 2157 2158 2159 2160
  do
    rm -r my_folder_name/Afgeleiden/$folder/$subfolder
  done
done

* increment folders:

for folder in JP2 JPG TIF
do
  for (( subfolder = 1036; subfolder <= 1062; ++subfolder ))
  do
    rm -r my_folder_name/Afgeleiden/$folder/$subfolder
  done
done

* increment files:

for folder in JP2 JPG TIF
do
  for (( file = 489; file <= 981; ++file ))
  do
    rm -r my_folder_name/Afgeleiden/$folder/0001244$file.${folder,,}
  done
done