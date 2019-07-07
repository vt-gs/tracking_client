#!/usr/bin/env python
#version 2.1

import socket
import os
import string
import sys
import time
import argparse
import datetime
import json
from binascii import *
from track_gui import *
from vtp import *

if __name__ == '__main__':
    """ Main entry point to start the service. """
    startup_ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    #--------START Command Line argument parser------------------------------------------------------
    parser = argparse.ArgumentParser(description="VTGS Tracking Client",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    cwd = os.getcwd()
    cfg_fp_default = '/'.join([cwd, 'config'])
    cfg = parser.add_argument_group('Daemon Configuration File')
    cfg.add_argument('--cfg_path',
                       dest='cfg_path',
                       type=str,
                       default='/'.join([os.getcwd(), 'config']),
                       help="Daemon Configuration File Path",
                       action="store")
    cfg.add_argument('--cfg_file',
                       dest='cfg_file',
                       type=str,
                       default="track-gui_config.json",
                       help="Daemon Configuration File",
                       action="store")
    opt = parser.add_argument_group('User Command Line Options')
    opt.add_argument('--ip',
                       dest='ip',
                       type=str,
                       default=None,
                       help="Tracking Daemon IP Address",
                       action="store")
    opt.add_argument('--port',
                       dest='port',
                       type=int,
                       default=None,
                       help="Tracking Daemon Port Number",
                       action="store")
    opt.add_argument('--ssid',
                       dest='ssid',
                       type=str,
                       default="fed-vu",
                       help="Startup Subsystem ID",
                       action="store")
    opt.add_argument('--uid',
                       dest='uid',
                       type=str,
                       default=None,
                       help="Startup Subsystem ID",
                       action="store")

    args = parser.parse_args()
#--------END Command Line argument parser------------------------------------------------------
    os.system('reset')
    fp_cfg = '/'.join([args.cfg_path,args.cfg_file])
    if not os.path.isfile(fp_cfg) == True:
        print 'ERROR: Invalid Configuration File: {:s}'.format(fp_cfg)
        sys.exit()
    print 'Importing configuration File: {:s}'.format(fp_cfg)
    with open(fp_cfg, 'r') as json_data:
        cfg = json.load(json_data)
        json_data.close()

    if args.uid == None:
        print 'No User ID Specified'
        print 'Please Specify a User ID'
        print 'Exiting...'
        sys.exit()
    else:
        cfg.update({'uid':args.uid})

    if args.ip != None:
        cfg.update({'daemon_ip':args.ip})


    args.ssid = args.ssid.lower()
    #if (options.ssid != 'VUL') and (options.ssid != '3M0') and (options.ssid != '4M5') and (options.ssid != 'WX'):
    ssid_list = []
    for ssid in cfg['ssid']: ssid_list.append(ssid['name'])
    if args.ssid is not None:
        if args.ssid not in ssid_list:
            print 'INVALID SSID Specified'
            print 'Valid Options: ', ssid_list
            print 'Please Specify a valid SSID'
            print 'Exiting...'
            sys.exit()
        else:
            cfg.update({'startup_ssid':args.ssid})

    print json.dumps(cfg, indent=4)

    #track = vtp(options.ip, port, options.uid, options.ssid, 2.0)
    track = vtp(cfg)

    app = QtGui.QApplication(sys.argv)
    win = MainWindow(cfg)
    win.set_callback(track)
    #win.setGpredictCallback(gpred)
    sys.exit(app.exec_())
    sys.exit()
