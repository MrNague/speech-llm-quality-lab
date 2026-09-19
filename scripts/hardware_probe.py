"""Offline E01 inventory. Does not collect usernames, hostname, or absolute paths."""
import argparse
import ctypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess


def probe():
    memory=None
    if platform.system()=='Windows':
        class MemoryStatus(ctypes.Structure):
            _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(n,ctypes.c_ulonglong) for n in ['total','available','page_total','page_available','virtual_total','virtual_available','extended']]
        status=MemoryStatus();status.length=ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):memory=status.total
    else:
        try:memory=os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')
        except (ValueError,OSError,AttributeError):pass
    cpu=platform.processor() or platform.machine()
    if platform.system()=='Linux':
        try:
            cpu=next(line.split(':',1)[1].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name'))
        except (OSError,StopIteration):pass
    gpu=[]
    if shutil.which('nvidia-smi'):
        try:
            result=subprocess.run(['nvidia-smi','--query-gpu=name,memory.total','--format=csv,noheader'],capture_output=True,text=True,timeout=10)
            if result.returncode==0:gpu=result.stdout.strip().splitlines()
        except (OSError,subprocess.TimeoutExpired):pass
    return dict(timestamp=datetime.now(timezone.utc).isoformat(),os=platform.system(),os_release=platform.release(),architecture=platform.machine(),cpu=cpu,logical_cpus=os.cpu_count(),ram_bytes=memory,free_disk_bytes=shutil.disk_usage('.').free,python=platform.python_version(),nvidia_gpu=gpu,note='Inventory only; empty GPU list does not prove absence. No inference benchmark. Container resources may differ from host.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('artifacts/hardware.json'));args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(probe(),indent=2)+'\n',encoding='utf-8')
    print('Hardware inventory written; E01 requires reference-device confirmation.')
