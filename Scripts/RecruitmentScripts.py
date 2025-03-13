import pandas as pd
import datetime

""" Export to CSV "Including Ineligible" from sharepoint """


today = datetime.date.today() #datetime.date(2025, 2, 28) #datetime.date.today()



class RecruitmentScripts():
    def __init__(self, file, cutoff):
        self.recruitment = pd.read_csv(file)

        self.recruitment["16 Window Start"] = pd.to_datetime(self.recruitment["16 Window Start"])
        self.recruitment["16 Window Start"] = self.recruitment["16 Window Start"].dt.date

        self.recruitment["36 Window End"] = pd.to_datetime(self.recruitment["36 Window End"])
        self.recruitment["36 Window End"] = self.recruitment["36 Window End"].dt.date

        self.recruitment["Scheduled WIC Visit %231"] = pd.to_datetime(self.recruitment["Scheduled WIC Visit %231"])
        self.recruitment["Scheduled WIC Visit %231"] = self.recruitment["Scheduled WIC Visit %231"].dt.date

        self.recruitment["Rescheduled WIC Visit %231"] = pd.to_datetime(self.recruitment["Rescheduled WIC Visit %231"])
        self.recruitment["Rescheduled WIC Visit %231"] = self.recruitment["Rescheduled WIC Visit %231"].dt.date

        self.cutoff = cutoff
        self.today = datetime.date.today()

    def totalScreened(self):
        totalRecords = self.recruitment["Name"]
        return len(totalRecords)

    #Moms not yet in window
    def getNotInWindow(self):
        notInWindow = self.recruitment[(self.recruitment["16 Window Start"] > self.cutoff)]
        return len(notInWindow)
        #print(notInWindow["16 Window Start"])

    #Moms in window
    def getInWindow(self):
        inWindow = self.recruitment[(self.recruitment["16 Window Start"] <= self.cutoff) & (self.cutoff <= self.recruitment["36 Window End"]) & (((self.recruitment["Showed Visit"] != "Yes") | (self.recruitment["Showed Visit"].isna()))) & (((self.recruitment["Showed Res. Visit"] != "Yes") | (self.recruitment["Showed Res. Visit"].isna())))]
        return len(inWindow)
        #print(inWindow["16 Window Start"])

    #Moms out of window (Requires Ineligible File)
    def missedWindow(self):
        missedWindow = self.recruitment[(self.recruitment["36 Window End"] < self.cutoff) & (((self.recruitment["Showed Visit"] != "Yes") | (self.recruitment["Showed Visit"].isna()))) & (((self.recruitment["Showed Res. Visit"] != "Yes") | (self.recruitment["Showed Res. Visit"].isna())))]
        return len(missedWindow)

    def numberOfScheduledMothers(self):
        nonDate = datetime.date(1899, 12, 30)
        numOfScheduled = self.recruitment[(self.recruitment["Scheduled WIC Visit %231"] != nonDate)]
        return len(numOfScheduled["Scheduled WIC Visit %231"])

    def averageNumberOfTimesScheduled(self):
        validRows = self.recruitment["%23 of Times Scheduled"].dropna()
        n = len(validRows)
        timesScheduled = round((validRows.sum() / n if n > 0 else 0), 1)
        return timesScheduled


    if __name__ == "__main__":
        totalScreened()
        missedWindow()
        getInWindow()
        getNotInWindow()
        numberOfScheduledMothers()
        averageNumberOfTimesScheduled()
