# coding:utf-8

import subprocess
import sys
import time 
import getopt
import os
import json

split_str = "##############################NEXT PROBE##############################"

def Usage():
	print('''
 ###################################################################
 #                     nmap-service-probes-patch                   #
 ###################################################################
 -------------------------------------------------------------------
 Usage:
 python %s [options] ...

 -n <nmap>         nmap-service-probes file
 -p <nmap-patch>   nmap-service-probes-patch file
 -------------------------------------------------------------------
	'''%os.path.basename(__file__))
	sys.exit()

 
def nmap_patch(nmap_probes_list,patch_json):
	patch_nmap_probe_obj = open(nmap_file+"_patch_"+time.strftime("%Y%m%d%H%M", time.localtime()),"a",encoding="utf-8")

	for patch in patch_json["apps"]:
		probe = patch["probe"]
		src_conf = patch["src_conf"]
		dst_conf = patch["dst_conf"]
		action = patch["action"]

		for n in range(len(nmap_probes_list)):
			probe_data = nmap_probes_list[n]
			if probe in probe_data:
				if action == "update":
					if src_conf in probe_data:
						probe_data = probe_data.replace(src_conf,dst_conf)
					else:
						action = "add"
				if action == "add":
					probe_data += '\n'+dst_conf+'\n'
				nmap_probes_list[n] = probe_data

	for n in range(len(nmap_probes_list)):
		if n == 0:
			probe_data = nmap_probes_list[n]
		else:
			if probe_data[-1] != "\n":
				probe_data = "\n"+split_str+nmap_probes_list[n]
			else:
				probe_data = split_str+nmap_probes_list[n]		
		patch_nmap_probe_obj.write(probe_data)
		patch_nmap_probe_obj.flush()

def main():

	with open(nmap_file,"r",encoding="utf-8") as n_obj:
		nmap_probes_list = n_obj.read().split(split_str)

	with open(patch_file,"r",encoding="utf-8") as p_obj:
		patch_json = json.loads(p_obj.read().replace('\\','\\\\'))

	nmap_patch(nmap_probes_list,patch_json)

if __name__ == '__main__':

	nmap_file = 'nmap-service-probes'
	patch_file = 'nmap-service-probes-patch.json'

	try:
		opts,args = getopt.getopt(sys.argv[1:],'n: p:')
	except:
		Usage()

	for o, a in opts:
		if o == "-n":
			nmap_file = str(a)
		if o == "-p":
			patch_file = str(a)

	if nmap_file and patch_file:
		main()
	else:
		Usage()