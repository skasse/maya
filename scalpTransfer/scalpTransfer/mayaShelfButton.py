import sys, os
paths = ["C:/Scripts/maya/xg2igs/xg2igs", "C:/Scripts/maya/scalpTransfer/scalpTransfer"]

for path in paths:
    if not path in sys.path:
    	sys.path.append(path)

import xg2Ov, xg_scalp_transfer
# help(xg2Ov)
# help(xg_scalp_transfer)

xg_scalp_transfer.xg_scalp_transfer()
xg2Ov.igs2Usd()