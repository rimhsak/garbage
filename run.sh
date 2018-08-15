#!/bin/bash

NUM_CPU=${1:-1}


for i in `seq 0 $(( $NUM_CPU - 1 ))`
do
    rm -rf ./data/$i
    mkdir ./data/$i
    cp ./data/*.txt ./data/$i/
    awk -v num=0 '{if(NR%1 == num){print $0}}' ./data/ptb.train.txt | shuf > ./data/$i/ptb.train.txt
    awk -v num=0 '{if(NR%1 == num){print $0}}' ./data/ptb.char.train.txt| shuf > ./data/$i/ptb.char.train.txt
done

ps_hosts="127.0.0.1:1111"
worker_hosts=""
for i in `seq -w 0 $(($NUM_CPU - 2 ))`
do
    worker_hosts="${worker_hosts}127.0.0.1:300$i," # 2222,127.0.0.1:3333,127.0.0.1:4444,127.0.0.1:5555"
done
worker_hosts="${worker_hosts}127.0.0.1:300$(( $NUM_CPU - 1 ))"

cat /dev/null > pids

# run ps
python ./ptb_word_lm.py --job_name=ps --task_index=0 --ps_hosts=$ps_hosts --worker_hosts=$worker_hosts &
echo $! >> pids 
sleep 1

# run worker
for i in `seq 0 $(( $NUM_CPU - 1 ))`
do
    python ./ptb_word_lm.py --job_name=worker --task_index=$i --ps_hosts=$ps_hosts --worker_hosts=$worker_hosts --data_path=./data/$i &
    echo $! >> pids 

done


