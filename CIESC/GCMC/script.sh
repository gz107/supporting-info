#! /bin/sh -f
export RASPA_DIR=/thfs1/home/junqiang/users/wanghui/gz/RASPA2-master/raspa
export DYLD_LIBRARY_PATH=/thfs1/home/junqiang/users/wanghui/gz/RASPA2-master/raspa/lib
export LD_LIBRARY_PATH=/thfs1/home/junqiang/users/wanghui/gz/RASPA2-master/raspa/lib
$RASPA_DIR/bin/simulate $1
