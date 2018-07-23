# FileTransferClient

A simple client that connects to SSH servers and transfers files of a specified directory in both directions.
This client is meant to transfer all files of a directory to another device to automate file transfer routines.
The purpose is to transfer files from a small Data Mining server (for example a Raspberry Pi) to another device in the network to further process the data. That is why the client can easily be run in automated cronjobs.

Usage:

./FileTransferClient.py [-s | -g] <host/IP> <port> <username> <password> <source directory> <output directory> (--keepAfterTransfer)
  
  -s: sending data from client to server
  -g: receiving data from server
  --keepAfterTransfer (optional): keep the files in the source directory after transfer
