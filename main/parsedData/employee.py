import datetime

try:
    from job import Job
except ImportError:
    from .job import Job

class Employee: 
    def __init__(self, jobType):
        self.__jobType = jobType
        self.__ssn = 0
        self.__jobs = []
    
    def addJob(self, jobType): 
        for job in self.__jobs: 
            if job.type() == jobType: 
                return job
        newJob = Job(jobType)
        self.__jobs.append(newJob)
        return newJob
    
    def totalJobHours(self, jobType): 
        for job in self.__jobs: 
            if job.type() == jobType: 
                return job.totalHours()


    