#!/bin/bash

echo -e '\e[1mDetecting Hardware Type ...\e[0m'

if ./lshw.py supermicro-compute.xml > /dev/null 2>&1; then
  echo -e ' \e[1;32m*\e[0m Supermicro compute node'
elif ./lshw.py supermicro-storage.xml > /dev/null 2>&1; then
  echo -e ' \e[1;32m*\e[0m Supermicro storage node'
else
  echo -e ' \e[1;31m!\e[0m Unknown node type'
fi

