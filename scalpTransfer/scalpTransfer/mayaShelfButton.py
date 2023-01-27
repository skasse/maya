import sys, os
paths = ["C:/Scripts/maya/scalpTransfer/scalpTransfer"]

for path in paths:
    if not path in sys.path:
    	sys.path.append(path)

import xg_to_ov, xg_scalp_transfer
# help(xgen_to_ov)
# help(xg_scalp_transfer)

xg_scalp_transfer.xg_scalp_transfer()
xg_to_ov.main()