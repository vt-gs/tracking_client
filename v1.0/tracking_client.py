#!/usr/bin/env python
#version 2.1

import socket
import os
import string
import sys
import time
from optparse import OptionParser
from binascii import *
from track_gui import *
from vtp import *

if __name__ == '__main__':
    startup_ts = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
	#--------START Command Line option parser------------------------------------------------------
    parser = argparse.ArgumentParser(description="VTGS Tracking Daemon",
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
                        dest="cfg_file" ,
                        action = "store",
                        type = str,
                        default="fed_vu_config.json" ,
                        help = 'config file')

    args = parser.parse_args()
    #--------END Command Line option parser------------------------------------------------------
    print "args", args
    cfg_fp = '/'.join([args.cfg_path, args.cfg_file])
    print "config file:", cfg_fp
    with open(cfg_fp, 'r') as cfg_f:
        cfg = json.loads(cfg_f.read())

    cfg.update({'startup_ts':startup_ts})
    cfg['service'].update({'ssid':cfg['ssid']})
    cfg['service'].update({'log_path':cfg['log_path']})
    cfg['md01'].update({'ssid':cfg['ssid']})
    cfg['md01'].update({'log_path':cfg['log_path']})
    print json.dumps(cfg, indent=4)

    track = vtp(options.ip, port, options.uid, options.ssid, 2.0)

    app = QtGui.QApplication(sys.argv)
    win = MainWindow(options)
    win.set_callback(track)
    #win.setGpredictCallback(gpred)
    sys.exit(app.exec_())
    sys.exit()
