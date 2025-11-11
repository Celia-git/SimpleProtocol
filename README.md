# Simple Protocol Client-Server   
## Overview   
This project implements a simple client-server network protocol where the client sends commands to turn on/off an LED light connected to the server. 

The communication uses TCP sockets with a custom packet structure including version, message type, and message length headers.   

 This simple protocol demo requires coordinated client-server execution on networked machines with open ports and correct IP addresses, ideally using bridged network mode in virtualized environments for realistic remote testing.    


---   
## Prerequisites   
- Python 3.x installed on both server and client machines. - Both machines (or VMs) should be network-reachable (e.g., via bridged networking on VMs). 
- - Network port (default 30000) must be open and reachable.   
---   
## Running the Server   
1. On the server machine, run the server script specifying the listening port and log file location: 

```python3 lightserver.py -p 30000 -l server_log.txt```

 2. The server will start listening on all interfaces (0.0.0.0) and log connections and commands.   
 ---   
 ## Running the Client   
 1. On the client machine, run the client script with the server IP, server port, and log file location: 

```python3 lightclient.py -s <SERVER_IP> -p 30000 -l client_log.txt```

- Replace `<SERVER_IP>` with the server’s IP address reachable from the client.   
 2. The client sends a "HELLO" message, waits for the server response, then sends a command (LIGHTON or LIGHTOFF).   
 ---   
 ## Network Setup for Testing   
 - For virtual machines, set network adapters to **Bridged Mode** to ensure each VM has a unique IP on the local network. 
 - - Ensure both server and client machines can ping each other using their bridged IP addresses. 
 - - No firewall should block TCP port 30000 in either machine.   
 ---   

