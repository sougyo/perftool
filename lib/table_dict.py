def get():
  return {
    "sar-B": {
      "column_pattern": "pgpg",
    },
    "sar-b": {
      "column_pattern": "tps",
    },
    "sar-d": {
      "column_pattern": "svctm",
      "subkey_column": "DEV",
    },
    "sar-H": {
      "column_pattern": "kbhug",
    },
    "sar-I": {
      "column_pattern": "intr",
      "subkey_column": "INTR",
    },
    "sar-mCPU": {
      "column_pattern": "MHz",
      "subkey_column": "CPU",
    },
    "sar-nDEV": {
      "column_pattern": "xpck",
      "subkey_column": "IFACE",
    },
    "sar-nEDEV": {
      "column_pattern": "xerr",
      "subkey_column": "IFACE",
    },
    "sar-nSOCK": {
      "column_pattern": "sck",
    },
    "sar-nIP": {
      "column_pattern": "irec",
    },
    "sar-nEIP": {
      "column_pattern": "ihdrerr",
    },
    "sar-nICMP": {
      "column_pattern": "imsg",
    },
    "sar-nEICMP": {
      "column_pattern": "ierr",
    },
    "sar-nTCP": {
      "column_pattern": "passive",
    },
    "sar-nETCP": {
      "column_pattern": "atmptf",
    },
    "sar-nUDP": {
      "column_pattern": "idgm",
    },
    "sar-nEUDP": {
      "column_pattern": "atmptf",
    },
    "sar-q": {
      "column_pattern": "runq",
    },
    "sar-R": {
      "column_pattern": "frmpg",
    },
    "sar-r": {
      "column_pattern": "kbmem",
    },
    "sar-S": {
      "column_pattern": "kbswp",
    },
    "sar-u": {
      "column_pattern": "idle",
      "subkey_column": "CPU",
    },
    "sar-v": {
      "column_pattern": "inode",
      "subkey_column": "CPU",
    },
    "sar-W": {
      "column_pattern": "pswp",
    },
    "sar-w": {
      "column_pattern": "cswch",
    },
    "iostat": {
      "column_pattern": "rrqm",
      "subkey_column": "Device:",
      "time_regexp": "\d\d/\d\d/\d\d (\d\d:\d\d:\d\d)",
    },
    "top": {
      "column_pattern": "COMMAND",
      "subkey_column": "PID",
      "exact": "False",
      "time_regexp": "top \- (\d\d:\d\d:\d\d)",
    },
    "interrupts": {
      "column_pattern": "CPU",
      "subkey_column": "HEAD",
      "column_head": "HEAD",
      "column_tail": "TAIL",
      "exact": "False",
      "time_regexp": "^Time:\s+(\d\d:\d\d:\d\d)",
    },
    "numastat": {
      "column_pattern": "node0",
      "subkey_column": "HEAD",
      "column_head": "HEAD",
      "time_regexp": "^Time:\s+(\d\d:\d\d:\d\d)",
    },
    "ps": {
      "column_pattern": "PID",
      "subkey_column": "PID",
      "exact": "False",
      "time_regexp": "^Time:\s+(\d\d:\d\d:\d\d)",
    },
    "pidstat-d": {
      "column_pattern": "kB",
      "subkey_column": "PID",
      "exact": "False",
    },
    "slabinfo": {
      "column_pattern": "name",
      "subkey_column": "name",
      "exact": "False",
      "time_regexp": "^Time:\s+(\d\d:\d\d:\d\d)",
      "replace_old": "# name",
      "replace_new": "name",
    },
  }
