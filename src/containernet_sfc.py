#!/usr/bin/python3
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from json_register import register
from optparse import OptionParser
import os

setLogLevel('info')

def setLinks(net,links):
    for link in links:
        s1 = int(link[0])
        s2 = int(link[1])
        try:
            net.addLink(net.switches[s1],net.switches[s2])
            # print(link)
        except:
            pass

def topology(file='data/network_10.txt'):
    desc = ( 'Create a homogeneous virtual network with -n [N] nodes, default is 6.' )
    usage = ( 'sudo python containernet_sfc.py -n [number of nodes]\n')
    op = OptionParser( description=desc, usage=usage )

    # Options
    op.add_option( '--nodes', '-n', action="store", dest="nodes")
    op.add_option( '--topo', action="store", dest="file")

    options, _ = op.parse_args()

    if options.file:
        file = options.file
    nodes = set()
    with open (file,'r') as f:
        links = f.readlines()
    links = [link.split() for link in links]
    for link in links:
        for n in link:
            nodes.add(n)
    
    N = len(nodes) # default 10 of hosts in network
    if options.nodes:
        N = int(options.nodes)

    """Create a network"""
    net = Containernet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
 
    info("*** Creating nodes\n")    
    # info('*** Adding docker containers\n')
    # h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')#, dimage="lxr/snort:latest") #, dcmd="snort -i h1-eth0 -c /etc/snort/etc/snort.conf -A console")
    for i in range(N):
        n = i+1
        name = 'h'+str(n)
        vars()[name] = net.addHost(name, mac='00:00:00:00:00:{:0>2d}'.format(n), ip='10.0.0.{}/24'.format(n))

    info('*** Adding switches\n')
    # s1 = net.addSwitch( 's1', listenPort=6671 )
    for i in range(N):
        n = i+1
        name = 's'+str(n)
        port = 6670+n
        vars()[name] = net.addSwitch( name, listenPort=port )

    info('*** Adding controller\n')
    c7 = net.addController( 'c7', controller=RemoteController, ip='127.0.0.1', port=6633 )
 
    info("*** Creating links")    

    for i in range(N):
        n = i+1
        net.addLink(vars()['s'+str(n)], vars()['h'+str(n)]) # connect switch and its host
    # print(net.switches)
    setLinks(net,links)
        # if i != 0:
        #     net.addLink(vars()['s'+str(i)], vars()['s'+str(n)]) # switches connect to each other
        
    # h1.cmd('ifconfig h2-eth1 10.0.0.12 netmask 255.255.255.0')
    # h2.cmd('ifconfig h2-eth1 10.0.0.12 netmask 255.255.255.0')
    # h3.cmd('ifconfig h3-eth1 10.0.0.13 netmask 255.255.255.0')


    print ("*** Starting network")

    net.build()
    # h2.cmd('ip route add 10.0.0.1/32 dev h2-eth0; ip route add 10.0.0.5/32 dev h2-eth1')
    # h2.cmd('ip route add 10.0.0.253/32 dev h2-eth0; ip route add 10.0.0.254/32 dev h2-eth1')
    # h2.cmd('sudo arp -i h2-eth0 -s 10.0.0.253 01:02:03:04:05:06')
    # h2.cmd('sudo arp -i h2-eth1 -s 10.0.0.254 11:12:13:14:15:16')
    
    # h3.cmd('ip route add 10.0.0.1/32 dev h3-eth0; ip route add 10.0.0.5/32 dev h3-eth1')
    # h3.cmd('ip route add 10.0.0.253/32 dev h3-eth0; ip route add 10.0.0.254/32 dev h3-eth1')
    # h3.cmd('sudo arp -i h3-eth0 -s 10.0.0.253 01:02:03:04:05:06')
    # h3.cmd('sudo arp -i h3-eth1 -s 10.0.0.254 11:12:13:14:15:16')

    # h5.cmd('sudo arp -i h5-eth0 -s 10.0.0.253 01:02:03:04:05:06')
    for i in range(N):
        n = i+1
        name = 'h'+str(n)
        vars()[name].cmd('ip route add 10.0.0.253/32 dev '+name+'-eth0;') # ensure the register msg is sent from eth0
        vars()[name].cmd('arp -i h'+str(n)+'-eth0 -s 10.0.0.253 01:02:03:04:05:06;') # ensure the udp msg success

    c7.start()
    # s1.start( [c7] )
    for i in range(N):
        n = i+1
        name = 's'+str(n)
        vars()[name].start([c7])

    for i in range(N):
        n = i+1
        name = 'h'+str(n)
        reg_str = '\"{{name=vnf{}, vnf_id={}, type_id=1, group_id=1, iftype=3, bidirectional=False, geo_location=host{}.new.room}}\"'.format(n,n,n)
        vars()[name].cmd('src/json_register.py --reg='+reg_str) #+' -a 10.0.0.253 -p 30012 -n registration')

    print("*** Installing default SFC")
    os.system('curl -v http://127.0.0.1:8080/add_flow/1')

    print("*** Running CLI")
    CLI( net )
 
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    topology()
