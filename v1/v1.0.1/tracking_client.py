#!/usr/bin/env python3
#version 1.0.1

#import socket
import os
import string
import sys
import time
import datetime
import json
import argparse
from binascii import *

#from track_gui import *
#from vtp import *

if __name__ == '__main__':
    startup_ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
	#--------START Command Line option parser------------------------------------------------------
    parser = argparse.ArgumentParser(description="VTGS Tracking Client, v1.0.1",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #General Options
    cwd = os.getcwd()
    #sch_fp_default = '/'.join([cwd, 'schedule'])
    cfg_fp_default = '/'.join([cwd, 'config'])
    parser.add_argument("--cfg_fp"   ,
                        dest   = "cfg_path" ,
                        action = "store",
                        type   = str,
                        default=cfg_fp_default,
                        help   = 'config path')
    parser.add_argument("--cfg_file" ,
                        dest   ="cfg_file" ,
                        action = "store",
                        type   = str,
                        default="track-gui_config.json" ,
                        help   = 'config file')

    args = parser.parse_args()
    #--------END Command Line option parser------------------------------------------------------
    print("args", args)
    cfg_fp = '/'.join([args.cfg_path, args.cfg_file])
    print("config file:", cfg_fp)
    with open(cfg_fp, 'r') as cfg_f:
        cfg = json.loads(cfg_f.read())
    cfg.update({'startup_ts':startup_ts})

    log_name = '.'.join([cfg['ssid'],cfg['name'],'main'])
    cfg['main_log'].update({
        "path":cfg['log_path'],
        "name":log_name,
        "startup_ts":startup_ts
    })

    for key in cfg['thread_enable'].keys():
        cfg[key].update({'log':{}})
        log_name =  '.'.join([cfg['ssid'],cfg['name'],key])
        cfg[key].update({
            'ssid':cfg['ssid'],
            'main_log':cfg['main_log']['name']
        })
        cfg[key]['log'].update({
            'path':cfg['log_path'],
            'name':log_name,
            'startup_ts':startup_ts,
            'verbose':cfg['main_log']['verbose'],
            'level':cfg['main_log']['level']
        })

    main_thread = Main_Thread(cfg, name="Main_Thread")
    main_thread.daemon = True
    main_thread.run()
    sys.exit()

    #print(json.dumps(cfg, indent=4))
    # sys.exit()
    # track = vtp(options.ip, port, options.uid, options.ssid, 2.0)

    #app = QtGui.QApplication(sys.argv)
    #win = MainWindow(options)
    #win.set_callback(track)
    #win.setGpredictCallback(gpred)
    #sys.exit(app.exec_())
    #sys.exit()
