#!/usr/bin/env python

import subprocess, re, time, os, urllib2, signal
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
start=time.time()
file=open("log.txt","a")
file.write("########################Start########################\n")
ifname='wlp1s0'
ifname2='enp0s20f6'
subprocess.call('ifconfig '+ifname+' down', stdin=None, stdout=None, stderr=None, shell=True)
time.sleep(1)
subprocess.call('ip link set '+ifname+' up', stdin=None, stdout=None, stderr=None, shell=True)
time.sleep(3)
file.write("Scanning\n")
proc = subprocess.Popen('iwlist '+ifname+' scan', shell=True, stdout=subprocess.PIPE,)
stdout_str = proc.communicate()[0]
stdout_list=stdout_str.split('\n')
addresses=[]
channels=[]
frequencies=[]
for line in stdout_list:
  line=line.strip()
  #print line
  match=re.search('Address: (\S+)',line)
  if match:
    address=match.group(1)
  match=re.search('Channel:(\S+)',line)
  if match:
    channel=match.group(0)
  match=re.search('Frequency:(\S+)',line)
  if match:
    frequency=match.group(0)
  match=re.search('ESSID:"UB_CSI"',line)
  if match:
    #essid.append(match.group(0))
    #print match.group(0)
    addresses.append(address)
    channels.append(channel)
    frequencies.append(frequency)
#print essid
file.write("Scan Complete\n")
if len(addresses) > 0:
  file.write('Access Points Found with a UB_CSI ESSID = ' + str(len(addresses))+'\n')
  for i in range(0,len(addresses)):
    mac=addresses[i]
    file.write(mac+" "+channels[i]+" "+frequencies[i]+"\n")
    subprocess.call('ip link set '+ifname+' up', stdin=None, stdout=None, stderr=None, shell=True)
    connect_command ='iw dev '+ifname+' connect -w UB_CSI ' + mac + ' 2>/dev/null'
    proc=subprocess.Popen(connect_command, stdin=None, stdout=subprocess.PIPE, stderr=None, shell=True)
    stdout_str = proc.communicate()[0]
    #print stdout_str
    #print op.returncode
    match=re.search('connected to ' + mac.lower(), stdout_str)
    #print match.group(0)
    file.write(stdout_str+"\n")
    if proc.returncode==0 and match:
      if subprocess.call('ifconfig '+ifname+' 192.168.1.2 netmask 255.255.255.0 up', stdin=None, stdout=None, stderr=None,
shell=True)==0:
        proc=subprocess.Popen(['/home/root/linux-80211n-csitool-supplementary/netlink/log_to_file', mac], stdin=None, stdout=subprocess.PIPE, stderr=None, shell=False)
        time.sleep(1)
        subprocess.call('ping 192.168.1.1 -i 0.1 -c 10', stdin=None, stdout=subprocess.PIPE, stderr=None,shell=True)
        time.sleep(1)
        os.kill(proc.pid,signal.SIGINT)
        stdout_str= proc.communicate()[0]
        file.write(stdout_str+"\n")
        time.sleep(1)
        subprocess.call('ifconfig '+ifname+' down', stdin=None, stdout=None, stderr=None, shell=True)
      else:
	file.write('Cannot get IP address\n')
    else:
      subprocess.call('ip link set '+ifname+' down', stdin=None, stdout=None, stderr=None, shell=True)
else:
 file.write('No Access Points Found with a UB_CSI ESSID\n')
end=time.time()-start
file.write('Finished in '+str(end)+' seconds')
file.write('########################End########################\n')
file.close()




