#!/bin/bash
# script for submit
#-------------------
PPN=64 # process per node
j_name="test"
l_file=${j_name}.log  # log file 
f_file=Framework_name
u_file=Unitcell_size
#-------------------

set -e
# check
if [ ! -f $f_file ];then echo "No $f_file, exit"  && exit ;fi
if [ ! -f $u_file ];then echo "No $u_file, exit"  && exit ;fi
# 
f_line=`cat $f_file | wc -l`
u_line=`cat $u_file | wc -l`

# check
if [[ "$f_line" != "$u_line" ]];then
  echo "ERROR!!! $f_file $f_line lines != $u_file $u_line , exit" && exit
fi

#
export total_job=$f_line

echo "-----------------------"
echo "Submit start at `date +"%F %T"`"
echo "-----------------------"
echo "  summary:"
echo "    total job    : $total_job"
echo "    job per node : $PPN"
echo "-----------------------"
echo ""
# current_directory
CMD=`pwd`

# create job
i=1
echo "Create job $total_job, please wait a moment ..."
echo
while [ $i -le $total_job ]; do
  if [ -d a$i ];then
    echo "WARNNING!!! Found a$i, continue"
    let i++
    continue
  else
    echo "create job a$i"
    mkdir a$i
  fi
  
  sed "16s/.*/$(sed -n ''$i'p' Framework_name)/" simulation_ads > temp_0
  sed "17s/.*/$(sed -n ''$i'p' Unitcell_size)/" temp_0 > temp_1
  sed "18s/.*/$(sed -n ''$i'p' VF)/" temp_1 > a$i/simulation.input


  cp ./script.sh a$i
  let i++
done

if [ -f temp_1 ];then rm temp_1; fi

# create submit script
j_start=1
j_end=1
j=1
loop=1

echo
echo "Create job submit script , please wait a moment ..."
echo
while [ $j_end -le $total_job ];do
  j_end=`expr $loop \* $PPN`
  if [ $j_end -gt $total_job ];then
    j_end=$total_job
  fi
# # creat file
  s_file=${j_name}_${j_start}_${j_end}.sh
  s_file_log=${j_name}_${j_start}_${j_end}.log
  s_file_err=${j_name}_${j_start}_${j_end}.err
  echo "create job submit script $s_file"
cat > $s_file << EOF
#!/bin/bash
#SBATCH -o $s_file_log
#SBATCH -e $s_file_err
EOF
  
  for((j=$j_start; j<$j_end; j++))
  do
    echo "cd $CMD/a$j ; sh script.sh & " >> $s_file
  done

  echo "wait" >> $s_file
  echo "echo \"Slurm job \$SLURM_JOBID Finish at \`date +\"%F %T\"\`, job id $j_start - $j_end \" >> $CMD/$l_file" >> $s_file

  let loop++
  j_start=`expr $j_end + 1`

  if [ $j_end -eq $total_job ];then break; fi

done

# submit_job
echo 
>$l_file
echo "==========================" >> $l_file
echo "submit log file:" >> $l_file
echo "==========================" >> $l_file
echo "  total_job    : $total_job" >> $l_file
echo "  job per node : $PPN" >> $l_file
echo "==========================" >> $l_file
echo "subimit details:" >> $l_file


#
j_start=1
j_end=1
j=1
loop=1

echo
echo "Submit job, please wait a moment ..."
echo
while [ $j_end -le $total_job ];do
  j_end=`expr $loop \* $PPN`
  if [ $j_end -gt $total_job ];then
    j_end=$total_job
  fi
  s_file=${j_name}_${j_start}_${j_end}.sh
  mytime=`date +"%F %T"`
  #slurmid=$(echo sbatch -N 1 -n $PPN -p thcp1 $s_file)
  slurmid=`yhbatch -N 1 -n $PPN -p thcp1 $s_file`
  echo $slurmid
  echo "  $mytime $slurmid $s_file" >> $l_file
  let loop++
  j_start=`expr $j_end + 1`
  if [ $j_end -eq $total_job ]; then break ; fi
done
echo "==========================" >> $l_file

echo 
echo "-----------------------"
echo "Submit Finish at `date +"%F %T"`"
echo "-----------------------"





