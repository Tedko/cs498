#!/usr/local/bin/python3
import Pilot

# f = open('output','r+')
#for i in range(0,5):
    # f.write(str(i))
    # f.write("time\n")
a=Pilot.Pilot(rc=True)
a.start()
a.grade()
    # print(a.grade(),file=f)
