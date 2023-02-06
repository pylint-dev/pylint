import subprocess

proc = subprocess.Popen(
    ['ls', '/home'],
    preexec_fn=lambda: print('Some actions'),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
