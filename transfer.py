# Project Name: CIS 41B - Lab 2:  Data Analysis/Visualization and GUI, using numpy, matplotlib, tkinter
# Name :        Yin Chang
# Module:       transfer.py
# Discription:  Takes care of the data analysis and visualization

import csv
import numpy as np
import matplotlib.pyplot as plt
import os

'''-------------------Defining Global Variables--------------------'''
filepath = os.path.dirname(__file__)

# Contains all the CA community college names
COLLEGE_NAME = os.path.join(filepath, "transferCC.csv")
# Contains the academic years for the past 11 years, from 2008-2009 to 2018-2019
YEARS = os.path.join(filepath, "transferYear.csv")
# Contains the transfer rate for each community college for the past 11 years.
RATE = os.path.join(filepath, "transferData.csv")


'''-------------------Defining Global Function--------------------'''


def printData(fct):
    """ When applied to a function or method, will print to the output screen the return value of the function."""
    def printOut(*arg, **kwarg):
        result = fct(*arg, **kwarg)
        print(result)
    return printOut


'''-------------------Defining Transfer Class--------------------'''


class Transfer():
    def __init__(self):
        """ Read data from all 3 input files and store in a numpy array or Python container as appropriate."""
        self._communityCollege, self._transferYear, self._transferRate = self._readInData()

    def _readInData(self):
        """ Read in the three file """
        with open(COLLEGE_NAME, encoding="latin-1") as infile:
            readCC = infile.read()                      # Read in the whole file at once
            # Remove the last new line from str
            readCC = readCC.rstrip("\n")
        communityCollege = readCC.split("\n")  # Put the data into a list
        with open(YEARS) as infile:
            readTy = infile.read()                      # Read in the whole file at once
            # Remove the last new line from str
            readTy = readTy.rstrip("\n")
            academicYear = readTy.split(",")      # Put the data into a list
        transferRate = np.loadtxt(RATE, dtype=int, delimiter=",")

        return(communityCollege, academicYear, transferRate)

    @printData
    def plotTransferTrend(self):
        """Plot the total transfer trend over the given years and return the total transfer array."""
        transferTrend = np.sum(self._transferRate, 0)
        plt.plot(np.arange(1, 12), transferTrend, "-*", label="total")
        # Add a title
        plt.title("Number of transfers")
        # Add y-axis label
        plt.ylabel("Transfers")
        plt.xticks(np.arange(1, 12), self._transferYear,
                   rotation=90)  # Add x-ticks as academic years
        plt.tight_layout()
        plt.legend(loc="best")
        return transferTrend

    @printData
    def plotEnrollmentTrend(self, *args):
        """Plot the enrollment trend for one or more community colleges and for the average enrollment."""
        averageEnrollment = np.mean(self._transferRate, 0)
        plt.plot(np.arange(1, 12), averageEnrollment,
                 label="Average Enrollment")
        for value in args:
            # Add a legend that shows the college names
            collegeName = self._communityCollege[value]
            collegeValue = self._transferRate[value, :]
            plt.plot(np.arange(1, 12), collegeValue, label=collegeName)
        # Add a title
        plt.title("Enrollment Trend")
        # Add y-axis label
        plt.ylabel("Enrollments")
        plt.xticks(np.arange(1, 12), self._transferYear,
                   rotation=90)  # Add x-ticks as academic years
        plt.tight_layout()
        plt.legend(loc="best")
        return averageEnrollment

    @printData
    def plotTopTenTransfer(self):
        """Plot the total transfer trend over the given years and return the total transfer array."""
        totalTransfer = np.sum(self._transferRate, 1)
        # Get the Top 10 number
        topTenNum = list(totalTransfer[np.argsort(totalTransfer)[-10:]])
        # Get the Top 10 index
        topTenIndex = list(np.argsort(totalTransfer)[-10:])
        # Create a list with Top 10 college name
        topTenName = [self._communityCollege[item] for item in topTenIndex]

        plt.bar(topTenName, topTenNum, align="center")
        # Add a title
        plt.title("The transfer numbers for the 10 colleges")
        # Add y-axis label
        plt.ylabel("Transfer numbers")
        # Add x-ticks as academic years   # Add y-axis label
        plt.xticks(rotation=90)
        plt.tight_layout()
        return topTenNum

    def getCC(self):
        """ A getter for the communityCollege array """
        return self._communityCollege


def main():
    """  A main test driver which will do the unit testing"""
    a = Transfer()
    a.plotTransferTrend()
    a.plotEnrollmentTrend(0, 1)
    a.plotTopTenTransfer()

# main()
