import pandas as pd
import datetime

# Total: In window, missed window
# Cuttoff (Input i.e Todays Date) Total number whos window has closed: Break down of Complete/Missed 


class EnrollmentScripts():
    def __init__(self, file, cutoff):
        self.enrollment = pd.read_csv(file)
        self.cutoff = cutoff

        self.enrollment["WIC %232 End"] = pd.to_datetime(self.enrollment["WIC %232 End"])
        self.enrollment["WIC %232 End"] = self.enrollment["WIC %232 End"].dt.date

        self.enrollment["WIC %232 Start"] = pd.to_datetime(self.enrollment["WIC %232 Start"])
        self.enrollment["WIC %232 Start"] = self.enrollment["WIC %232 Start"].dt.date

        self.today = datetime.date.today()


    #Total number of screened participants
    def totalRecords(self):
        return len(self.enrollment)

    #Total Completed
    def wicVisitComplete(self):
        complete = self.enrollment[(self.enrollment["Showed Visit"] == "Yes") | (self.enrollment["Showed Res. Visit"] == "Yes")]
        return len(complete)

    #Cutoff of Today Numbers
    def todayCompleted(self):
        todayCompleted = self.enrollment[(self.enrollment["WIC %232 End"] <= self.cutoff) & ((self.enrollment["Showed Visit"] == "Yes") | (self.enrollment["Showed Res. Visit"] == "Yes"))]
        return len(todayCompleted)

    def todayMissed(self):
        todayMissed = self.enrollment[(self.enrollment["WIC %232 End"] <= self.cutoff) & ((self.enrollment["Showed Visit"] != "Yes") | (self.enrollment["Showed Visit"].isna())) & ((self.enrollment["Showed Res. Visit"] != "Yes") | (self.enrollment["Showed Res. Visit"].isna()))]
        return len(todayMissed)

    def inWindow(self):
        inWindow = self.enrollment[(self.enrollment["WIC %232 Start"] <= self.cutoff) & (self.enrollment["WIC %232 End"] >= self.cutoff) & ((self.enrollment["Showed Visit"] != "Yes") | (self.enrollment["Showed Visit"].isna())) & ((self.enrollment["Showed Res. Visit"] != "Yes") | (self.enrollment["Showed Res. Visit"].isna()))]
        return len(inWindow)

    def notYetInWindow(self):
        notYetInWindow = self.enrollment[(self.enrollment["WIC %232 Start"] >= self.cutoff)]
        return len(notYetInWindow)

    if __name__ == "__main__":
        totalRecords()
        wicVisitComplete()
        todayCompleted()
        todayMissed()
        inWindow()
        notYetInWindow()
