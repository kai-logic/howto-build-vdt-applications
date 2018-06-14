Job
===

Class JobView
-------------

---
GET
---

Will return a specific job.

Class JobsView
--------------

---
PUT
---

Search for jobs. Input::

    {key: value}

Voluntary keys::

    jobMetadata = Get the jobs which matches with the specified comma separated query,
                  "key=value,key2=value2."
    jobType = Type of jobs.
    state = The state of the jobs.
    metadata = Include job metadata with all jobs.
    starttimeFrom = Start time of the jobs, from this value.
    starttimeTo = Start time of the jobs, to this value.
    finishtimeFrom = Finish time of the jobs, from this value.
    finishtimeTo = Finish time of the jobs, to this value.

