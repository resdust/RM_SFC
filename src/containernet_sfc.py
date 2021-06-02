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
            print(link)
        # s1 = 'h'+str(int(link[0])+1)
        # s2 = 'h'+str(int(link[1])+1)
        # try:
        #     net.addLink(net.getNodeByName(s1),net,getNodeByName(s2))
        except:
            print('failed to add',link)
            pass

def topology(file='data/network_10.txt'):
    desc = ( 'Create a homogeneous virtual network with -n [N] nodes, default is 10.' )
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
    # net.addLink(vars()['s1'], vars()['s2'])
    # net.addLink(vars()['s2'], vars()['s3'])
    # net.addLink(vars()['s1'], vars()['s10'])
    # net.addLink(vars()['s2'],vars()['s6'])
    # net.addLink(vars()['s4'],vars()['s1'])
        # if i != 0:
        #     net.addLink(vars()['s'+str(i)], vars()['s'+str(n)]) # switches connect to each other

    print ("*** Starting network")

    net.build()
    # h2.cmd('ip route add 10.0.0.253/32 dev h2-eth0; ip route add 10.0.0.254/32 dev h2-eth1')
    # h2.cmd('sudo arp -i h2-eth0 -s 10.0.0.253 01:02:03:04:05:06')
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

    ### Sqlite already have the vnf information. Quote to reduce traffic
    """for i in range(N):
        n = i+1
        name = 'h'+str(n)
        reg_str = '\"{{name=vnf{}, vnf_id={}, type_id=1, group_id=1, iftype=3, bidirectional=False, geo_location=host{}.new.room}}\"'.format(n,n,n)
        vars()[name].cmd('src/json_register.py --reg='+reg_str) #+' -a 10.0.0.253 -p 30012 -n registration')"""

    print("*** Installing default SFC")
    os.system('curl -v http://127.0.0.1:8080/add_flow/1')
    vars()['h1'].cmd('ping h10')

    print("*** Running CLI")
    CLI( net )
 
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    topology()
