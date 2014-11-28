#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7

import subprocess
import select
import Queue

Task_Queue = Queue.Queue()
poller = select.epoll()
tasks = {}
su = {}
MAX_JOBS = 16


def run(task, host):
    cmd = "ssh -n %s \"%s %s\"" % (host, task['cmd'], task['args'])
    print cmd
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    su[p.stdout.fileno()] = p
    tasks[p.stdout.fileno()] = task['name']
    poller.register(p.stdout, select.EPOLLHUP)


def add_task(task_desc):
    for i in xrange(1, task_desc['count'] + 1):
        cmd = task_desc['program']
        args = task_desc['args'] % i
        item = {'name': task_desc['name'] % i, 'cmd': cmd, 'args': args}
        Task_Queue.put(item)


class machine:
    '''The object for each machine in the machine queue'''

    def __init__(self, name, host=None, weight=1):
        self.name = name
        self.useed = false
        self.use_count = 0
        self.weight = weight

        




class machine_Queue:
    """Build a cycle queue in order to choose unused machine from the machine
        lists."""

    def __init__(self):
        self.size = 0
        self.queue = {}
        self.pos = 0

    def add_item_by_lambda(self, lambda_expr, size):
        self.size = size
        machine_list = map(lambda_expr, xrange(1, size + 1))
        self.queue = 

    def get(self):
        if self.size == 0:
            raise Exception("Machine Queue is empty!")

        pos = self.pos
        self.pos += 1
        if self.pos == self.size:
            self.pos = 0

        return self.queue[pos]

    def debug(self):
        return self.queue


def main():
    '''main: Main function

    Description goes here.
    '''

    task1 = {'count': 16, 'program': "cd ~/CMPUT429/as04/result; ./global.sh",
             'args': "%s ../500.txt", 'name': "global-500-%02d"}

    task2 = {'count': 16, 'program': "cd ~/CMPUT429/as04/result; ./nolock.sh",
             'args': "%s ../500.txt", 'name': 'nolock-500-%02d'}

    task3 = {'count': 16, 'program': "cd ~/CMPUT429/as04/result; ./local.sh",
             'args': "%s ../500.txt", 'name': 'local-500-%02d'}

    add_task(task1)
    add_task(task2)
    add_task(task3)

    Hosts = machine_Queue()
    expr = lambda x: "ug%02d" % (x + 1)
    Hosts.add_item_by_lambda(expr, 30)
    print Hosts.debug()

    print Task_Queue.qsize()

    jobs_count = 0

    while True:
        for fd, flags in poller.poll(timeout=1):
            poller.unregister(fd)
            print "\033[31m task [%s] done\033[0m" % tasks[fd]
            jobs_count -= 1

        while jobs_count < MAX_JOBS:
            if not Task_Queue.empty():
                # start a new job
                jobs_desc = Task_Queue.get()
                h = Hosts.get()
                print "\033[32m START JOB [%s] on Node <%s>\033[0m" % \
                    (jobs_desc['name'], h)
                jobs_count += 1
                run(jobs_desc, h)

            else:
                if jobs_count == 0:
                    print "\033[31m Done!\033[0m"
                    exit()
                else:
                    break

if __name__ == '__main__':
    main()
