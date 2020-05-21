#!/usr/bin/env bash
####################################################
# shell-name:  fwd-remote-controll                                   
#     author:  fwd                               
#   funciton:  fwd-remote-controll remote controll help                
#                                                   
#                                                   
#lastupdated:  05/20/20-09:14:49                            
#########+++++fwd+help: top1:help info+++++##########
#########++++-fwd+help: top2:help info-++++##########
#########+++--fwd+help: top3:help info--+++##########
####################################################
usage()
{
 ##----------------
 echo -e "\033[32m"
 ##----------------
 cat <<EOF
    [提示] 请打开如下目录 /Users/fwd/03-fwd_git/06-fly-higher-in-python/03-remote-cotroll
    [提示] 输入./remote-controll.py查看帮助
EOF
echo -e "\033[0m"
}
pathstr=$(dirname $(pwd))
echo "$pathstr"
replacestr="rmcmd_path=$pathstr"
sed -i "" "s;^rmcmd_path=.*;${replacestr};g" rmcmd.sh
cat rmcmd.sh
cp rmcmd.sh ~/bin/rmc
echo "安装完成,可以直接输入 rmc 进行操作"

