# syslog-stdout

Minimalistic syslog which just prints all messages received from /dev/log to standard out.
This is useful in docker containers where you don't want to install a full blown syslog daemon. It daemonises so does not interfere with the Docker containers primary purpose.

A Docker Entrypoint script should execute the syslog-stdout.py script before executing the primary program.

