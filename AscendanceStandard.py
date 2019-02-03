#! /usr/bin/python
# -*- coding:utf-8 -*-
class AscendanceStandard:  # Ascendance standard : 2.1 m/s au centre, parabole, 0 à 300m du centre
    def __init__(self):
        self.VMax=2.1
        self.R0=300
    def Vz(self,v,r):
        return max(0.,(v-self.VMax + (self.VMax*(1-(r*r/self.R0/self.R0)))))


print AscendanceStandard().Vz(3,0)
print AscendanceStandard().Vz(3,300)
print AscendanceStandard().Vz(2.1,300)
print AscendanceStandard().Vz(1.5,300)
print AscendanceStandard().Vz(5,400)