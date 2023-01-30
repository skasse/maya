import sys
import xg_to_ov, xg_scalp_transfer

paths = ["C:/Scripts/maya/scalpTransfer/scalpTransfer"]
[sys.path.append(p) for p in paths if p not in sys.path]

xg_scalp_transfer.main()
xg_to_ov.main()