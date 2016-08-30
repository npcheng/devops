import daemon

import  tranlate_name

with daemon.DaemonContext():
    tranlate_name.run()
