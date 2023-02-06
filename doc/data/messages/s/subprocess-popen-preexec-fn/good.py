import subprocess

proc = subprocess.Popen(
    ['script.sh'],  # a path to a script that will do a pre command
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
