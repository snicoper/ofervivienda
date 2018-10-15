#!/bin/bash

# Copia con rsync el directorio ~/backups al mi pc.

rsync -avz -e "ssh -p 6543" /home/snicoper/backups/ofervivienda.com snicoper@92.185.174.55:/home/snicoper/backups
