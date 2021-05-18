#!/usr/bin/env python3

from optparse import OptionParser
import socket
import sys
import json
import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main():
    desc = ( 'Send JSON Events' )
    usage = ( '%prog [options]\n'
              '(type %prog -h for details)' )
    op = OptionParser( description=desc, usage=usage )

    # Options
    op.add_option( '--reg', action="store", \
                     dest="register", help = "service registration information. Example: --reg='{ vnf_id=999, name=\'Yo-forwarder\', type_id=1, group_id=1, geo_location=\'server1.rack5.row17.room2\', iftype=1, bidirectional=False }'" )

    op.add_option( '--file', action="store",  \
                     dest="file", help = 'File containing the service registration information. It should follow the format of the registration as above i.e., starts with {..' )

    op.add_option( '--event-name', '-n', action="store",\
                     dest="event_name", help = 'The event name: Registration, Status, Deregistration'  )

    #op.add_option( '--event-value', '-l', action="store",\
    #                 dest="event_value", help = 'The event value.'  )

    op.add_option( '--addr', '-a', action="store",\
                     dest="addr", help = 'The address of the controller.' )

    op.add_option( '--port', '-p', action="store",\
                     dest="port", help = 'The port value of the controller.' )

    # Parsing and processing
    options, _ = op.parse_args()

    addr,port,event_name,reg_file,reg_str = options.addr, options.port, options.event_name, options.file, options.register

    register(reg_str, reg_file, event_name, addr, port)    

# return register string
def register(raw_str=None, reg_file=None, event_name='Registration', addr='10.0.0.253', port=30012):
    register_str=None

    if addr is None or port is None:
        # print('No IP address or Port information is given. Exiting.')
        # return
        addr = '10.0.0.253'
        port = 30012
        
    elif event_name is None:
        # print('No event name provided. Exiting.')
        # return
        event_name='Registration'
    # Open file if specified
    elif reg_file and raw_str:
        print('Can only specify one of (file,register)')
        return

    if reg_file:
        try:
            fd = open(reg_file, 'r')
        except IOError as err:
            logger.error('Error opening file: {}'.format(err))
            logger.error('Aborting.\n')
            sys.exit(1)
        content = fd.read()
        register_str = content

    elif raw_str:
        register_str = raw_str

    if register_str:
        print('register_str')
        # Parse register
        register_dict = dict(
            vnf_id = None,
            name=None,
            type_id=None,
            group_id=None,
            geo_location=None,
            iftype=None,
            bidirectional=None)

        parse_register_str(register_dict, register_str)

        json_message = dict(name=event_name,
                            register=register_dict)
        logger.info('register:'+str(register_dict))
    else:
        json_message = dict(name=event_name)
    # Create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        logger.error('Failed to create socket')
        sys.exit(1)
    logger.debug('json encode:')
    logger.debug(json.dumps(json_message).encode())
    s.sendto(json.dumps(json_message).encode(), (addr, int(port)))# Parsing and processing
    # register_str=None

    # if addr is None or port is None:
    #     print('No IP address or Port information is given. Exiting.')
    #     return
    # elif event_name is None:
    #     print('No event name provided. Exiting.')
    #     return
    # # Open file if specified
    # elif file and register:
    #     print('Can only specify one of (file,register)')
    #     return

    # elif file:
    #     try:
    #         fd = open(file, 'r')
    #     except IOError as err:
    #         logger.info('Error opening file: {}'.format(err))
    #         logger.debug('Aborting.\n')
    #         sys.exit(1)
    #     content = fd.read()
    #     register_str = content

    # elif register:
    #     register_str = register

    # if register_str:
    #     # Parse register
    #     register_dict = dict(
    #         vnf_id = None,
    #         name=None,
    #         type_id=None,
    #         group_id=None,
    #         geo_location=None,
    #         iftype=None,
    #         bidirectional=None)

    #     parse_register_str(register_dict, register_str)

    #     # json_message = dict(name=event_name,
    #     #                     register=register_dict)
    #     logger.debug('register:'+str(register_dict))
    # # else:
    # #     json_message = dict(name=event_name)
    # # Create socket
    # try:
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # except socket.error:
    #     logging.debug ('Failed to create socket')
    #     sys.exit(1)
    # s.sendto(json.dumps(json_message).encode(), (addr, int(port)))
    
    # return (register_str.strip(), addr, port)

def parse_register_str(register_dict, register_str):
    m = re.search("name=[\'\"]?([\w._-]+)",register_str)
    if m:
        register_dict['name'] = m.group(1)

    m = re.search("vnf_id=(\d+)\s*",register_str)
    if m:
        register_dict['vnf_id'] = m.group(1)


    m = re.search("type_id=(\d+)\s*",register_str)
    if m:
        register_dict['type_id'] = m.group(1)

    m = re.search("group_id=(\d+)\s*",register_str)
    if m:
        register_dict['group_id'] = m.group(1)

    m = re.search("geo_location=[\'\"]?([\w._-]+)",register_str)
    if m:
        register_dict['geo_location'] = m.group(1)

    m = re.search("iftype=(\d+)\s*",register_str)
    if m:
        register_dict['iftype'] = m.group(1)

    m = re.search("bidirectional=[\'\"]?(\w+)",register_str)
    if m:
        register_dict['bidirectional'] = m.group(1)

    logger.debug('register dict'+str(register_dict))

if __name__ == '__main__':
    main()
    # (json, addr, port) = register(file='data/forwarder1-1.txt', addr='10.0.0.254', port='30012', event_name='registration')
    # print(json)

