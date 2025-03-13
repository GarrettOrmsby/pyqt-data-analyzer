import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scripts.EnrollmentScripts import EnrollmentScripts
from Scripts.RecruitmentScripts import RecruitmentScripts


class Logic():
    def __init__(self, script_type, selected_scripts, file_path, cutoff_date):
        self.script_type = script_type
        self.selected_scripts = selected_scripts
        self.file_path = file_path
        self.cutoff_date = cutoff_date
        self.results = {}

    def runScripts(self):
        if self.script_type == "Enrollment":
            return self._run_enrollment_scripts()
        elif self.script_type == "Recruitment":
            return self._run_recruitment_scripts()
        else:
            raise ValueError(f"Unknow script type: {self.script_type}")
    
    def _run_enrollment_scripts(self):
        enrollment = EnrollmentScripts(self.file_path, self.cutoff_date)

        # Create a base mapping of script methods
        script_methods = {
            "Total Records": enrollment.totalRecords,
            "Total Completed Visits": enrollment.wicVisitComplete,
            "Total Missed Visits": enrollment.todayMissed,
            "Participants In Visit Window": enrollment.inWindow,
            "Particiapnts Not Yet In Visit Window": enrollment.notYetInWindow                                     
        }

        for script_name in self.selected_scripts:
            if script_name in script_methods:
                try:
                    self.results[script_name] = script_methods[script_name]()
                except Exception as e:
                    self.results[script_name] = f"Error: {str(e)}"
            # Special handling for date-specific script names
            elif "Completed Visits as of" in script_name:
                try:
                    self.results[script_name] = enrollment.todayCompleted()
                except Exception as e:
                    self.results[script_name] = f"Error: {str(e)}"
            else:
                self.results[script_name] = "Script not found"
        
        return self.results

    def _run_recruitment_scripts(self):
        recruitment = RecruitmentScripts(self.file_path, self.cutoff_date)

        script_methods = {
            "Total Screened Particiapnts": recruitment.totalScreened,
            "Participants that Missed Recruitment Window": recruitment.missedWindow,
            "Particiapnts In Recruitment Window": recruitment.getInWindow,
            "Participants Not Yet In Recruitment Window": recruitment.getNotInWindow,
            "Particiapnts Currently Scheduled": recruitment.numberOfScheduledMothers,
            "Average Number of Times Scheduled": recruitment.averageNumberOfTimesScheduled
        }

        for script_name in self.selected_scripts:
            if script_name in script_methods:
                try:
                    self.results[script_name] = script_methods[script_name]()
                except Exception as e:
                    self.results[script_name] = f"Error: {str(e)}"
                
            else:
                self.results[script_name] = "Script not found"
        
        return self.results