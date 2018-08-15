#!/bin/bash

for i in `seq 0 3`
do
    awk -v num=$i '{if(NR%4 == num){print $0}}' ptb.train.txt > $i/ptb.train.txt
    awk -v num=$i '{if(NR%4 == num){print $0}}' ptb.char.train.txt > $i/ptb.char.train.txt
done
