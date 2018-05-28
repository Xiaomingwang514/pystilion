######## 
pystilion
########

Python implementation of Postilion ISO 8583, including parser and utilities

This pystilion implementation is compatible with Postilion Realtime v5.6 speci-
fications, which contains ISO 8583 Postilion parser & message builders and some 
utilties for building payment applicaitons for communicating with Postilion 
Realtime.

########
Prerequisites
########

Pystilion has been built with Python v3.6.

######## 
sdk
######## 

The sdk package contains message parser & builder as well as tracing utility.

######## 
app/nidserver
########

This is an example TCP/IP server processing transactions from Postilion Realtime.
It accepts transactions and passes to a python script, where business logic can
be placed. 

To start the server, make sure current path "." is included in PYTHONPATH system varible 
and use the following command to start the server.

python .\pystilion\app\nidserver\server.py [configFile]

If the path to config file is not specified, .\config\config.ini will be used.

User should put business login in the .\config\filter.py

######## 
Test
########

Only functional tests are placed in .\test folder.

########
To Do
########

Comments in the code.
Automatic testing cases.