#!/usr/bin/env python3

import paramiko
from os import listdir
import argparse
import sys
import os
import stat

class FileTransferClient:

	def __init__(self,host,port,user,password):
		self.host=host
		self.port=port
		self.user=user
		self.password=password


	def start(self):
		print('Connecting...')
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(self.host, port=self.port, username=self.user, password=self.password)
		self.sftp = self.ssh.open_sftp()
		print('Connected')


	def send(self,src,dst):
		print('Sending ' + src + ' to ' + dst)
		self.sftp.put(src,dst)


	def close(self): 
		self.sftp.close()
		self.ssh.close()

	def recv(self,src,dst):
		print('Receiving ' + dst + ' from ' + src)
		self.sftp.get(src,dst)

def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-s', '--send', action='store_true', help='Send files to SSH server')
	group.add_argument('-g', '--get', action='store_true', help='Get files from SSH server')
	parser.add_argument('host', type=str, help='Hostname of SSH server')
	parser.add_argument('port', type=int, help='Port of SSH server')
	parser.add_argument('user', type=str, help='Username of SSH user')
	parser.add_argument('password', type=str, help='Password of SSH user')
	parser.add_argument('inputDir', type=str, help='Directory to transfer')
	parser.add_argument('outputDir', type=str, help='Output directory')
	parser.add_argument('--keepAfterTransfer', action='store_true', help='Keep files after transfer')
	args = parser.parse_args()

	client = None

	if args.send:
		for filename in listdir(args.inputDir):
			if os.path.isfile(args.inputDir + filename):
				if client == None:
					client = FileTransferClient(args.host,args.port,args.user,args.password)
					client.start()
				client.send(args.inputDir + filename, args.outputDir + filename)
				if not args.keepAfterTransfer:
					os.remove(args.inputDir + filename)
	if args.get:
		for fileattr in client.sftp.listdir_attr(args.inputDir):
			if not stat.S_ISDIR(fileattr.st_mode):
				if client == None:
					client = FileTransferClient(args.host,args.port,args.user,args.password)
					client.start()
				client.recv(args.inputDir + fileattr.filename, args.outputDir + fileattr.filename)
				if not args.keepAfterTransfer:
					client.sftp.remove(inputDir + fileattr.filename)
	if client != None:
		client.close()


if __name__ == '__main__':
	main()
