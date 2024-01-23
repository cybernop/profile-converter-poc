#!/bin/sh
docker volume create tmp
docker run --rm -v tmp:/mnt/shared gematik1/erp-cli-fhir erpf generate kbvbundle -n5
docker run --rm -v ./in:/in -v tmp:/out ubuntu /bin/sh -c 'cp /out/valid/* /in'
docker volume rm tmp
sudo chown $USER:$USER ./in/*
