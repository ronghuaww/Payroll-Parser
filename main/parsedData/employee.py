import datetime

try:
    from job import Job
except ImportError:
    from .job import Job

import sys


class Employee: 
    def __init__(self, name, ssn):
        self.name = name
        self.ssn = ssn
        self.jobs = []
    
    def addJob(self, name, wage): 
        newJob = Job(name, wage)
        self.jobs.append(newJob)

# e = Employee("j", "j")
# e.addJob("j", 23)
# print(e.jobs)

    