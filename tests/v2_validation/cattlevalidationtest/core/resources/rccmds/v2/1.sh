#!/bin/bash
ls *.yml | while read line
do
sed -i "" "s/ubuntu:14.04.3/microsoft\/nanoserver/g" ${line}
sed -i "" "s/ubuntu:14.04.2/microsoft\/nanoserver:sac2016/g" ${line}
done
