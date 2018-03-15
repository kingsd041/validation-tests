#!/bin/bash
#!/bin/bash
ls *.yml | while read line
do

sed -i "" "s/ubuntu:14.04.3/microsoft\/nanoserver/g" ${line}

done
