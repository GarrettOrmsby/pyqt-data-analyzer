import sys
import os
import datetime
import pandas as pd

# Add the parent directory to sys.path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scripts.EnrollmentScripts import EnrollmentScripts
from Scripts.RecruitmentScripts import RecruitmentScripts

def test_enrollment_scripts(file_path, cutoff_date):
    """Test EnrollmentScripts with a specific cutoff date"""
    print(f"\n=== Testing EnrollmentScripts with cutoff date: {cutoff_date} ===\n")
    
    try:
        # Create an instance of EnrollmentScripts
        enrollment = EnrollmentScripts(file_path, cutoff_date)
        
        # Test each method
        print("Total Records:")
        enrollment.totalRecords()
        
        print("\nWIC Visit Completed:")
        enrollment.wicVisitComplete()
        
        print(f"\nCompleted Visits as of {cutoff_date}:")
        enrollment.todayCompleted()
        
        print("\nTotal Missed Visits:")
        enrollment.todayMissed()
        
        print("\nParticipants in Window:")
        enrollment.inWindow()
        
        print("\nParticipants Not Yet in Window:")
        enrollment.notYetInWindow()
        
        print("\nEnrollment Scripts test completed successfully!")
    
    except Exception as e:
        print(f"Error testing EnrollmentScripts: {str(e)}")

def test_recruitment_scripts(file_path, cutoff_date):
    """Test RecruitmentScripts with a specific cutoff date"""
    print(f"\n=== Testing RecruitmentScripts with cutoff date: {cutoff_date} ===\n")
    
    try:
        # Create an instance of RecruitmentScripts
        recruitment = RecruitmentScripts(file_path, cutoff_date)
        
        # Set the cutoff date (since it's not set in the constructor)
        recruitment.cutoff = cutoff_date
        
        # Test each method
        print("Total Screened Participants:")
        recruitment.totalScreened()
        
        print("\nMoms Not Yet in Window:")
        recruitment.getNotInWindow()
        
        print("\nMoms In Window:")
        recruitment.getInWindow()
        
        print("\nMoms Missed Window:")
        recruitment.missedWindow()
        
        print("\nNumber of Scheduled Mothers:")
        recruitment.numberOfScheduledMothers()
        
        print("\nAverage Number of Times Scheduled:")
        recruitment.averageNumberOfTimesScheduled()
        
        print("\nRecruitment Scripts test completed successfully!")
    
    except Exception as e:
        print(f"Error testing RecruitmentScripts: {str(e)}")

def test_logic_class(enrollment_file, recruitment_file, cutoff_date):
    """Test the Logic class with both script types"""
    print(f"\n=== Testing Logic class with cutoff date: {cutoff_date} ===\n")
    
    from Logic.logic import Logic
    
    try:
        # Test Enrollment Logic
        enrollment_scripts = [
            "Total Records",
            "Total Completed Visits",
            "Total Missed Visits",
            f"Complete Visits as of {cutoff_date}",
            "Participants In Visit Window",
            "Particiapnts Not Yet In Visit Window"
        ]
        
        enrollment_logic = Logic(
            script_type="Enrollment",
            selected_scripts=enrollment_scripts,
            file_path=enrollment_file,
            cutoff_date=cutoff_date
        )
        
        print("Running Enrollment Scripts through Logic class:")
        enrollment_results = enrollment_logic.runScripts()
        
        print("\nEnrollment Results:")
        for script_name, result in enrollment_results.items():
            print(f"  {script_name}: {result}")
        
        # Test Recruitment Logic
        recruitment_scripts = [
            "Total Screened Particiapnts",
            "Participants that Missed Recruitment Window",
            "Particiapnts In Recruitment Window",
            "Participants Not Yet In Recruitment Window",
            "Particiapnts Currently Scheduled",
            "Average Number of Times Scheduled"
        ]
        
        recruitment_logic = Logic(
            script_type="Recruitment",
            selected_scripts=recruitment_scripts,
            file_path=recruitment_file,
            cutoff_date=cutoff_date
        )
        
        print("\nRunning Recruitment Scripts through Logic class:")
        recruitment_results = recruitment_logic.runScripts()
        
        print("\nRecruitment Results:")
        for script_name, result in recruitment_results.items():
            print(f"  {script_name}: {result}")
        
        print("\nLogic class test completed successfully!")
    
    except Exception as e:
        print(f"Error testing Logic class: {str(e)}")

if __name__ == "__main__":
    # Define test files and cutoff dates
    enrollment_file = "Files\WIC #2(1).csv"  # Replace with actual file path
    recruitment_file = "Files/Recruitment(3).csv"  # Replace with actual file path
    
    # Test with today's date
    today = datetime.date.today()
    
    # Test with a past date
    past_date = today - datetime.timedelta(days=90)
    
    # Test with a future date
    future_date = today + datetime.timedelta(days=90)
    
    # Run tests with different cutoff dates
    print("=== TESTING WITH TODAY'S DATE ===")
    test_enrollment_scripts(enrollment_file, today)
    test_recruitment_scripts(recruitment_file, today)
    test_logic_class(enrollment_file, recruitment_file, today)
    
    print("\n\n=== TESTING WITH PAST DATE ===")
    test_enrollment_scripts(enrollment_file, past_date)
    test_recruitment_scripts(recruitment_file, past_date)
    test_logic_class(enrollment_file, recruitment_file, past_date)
    
    print("\n\n=== TESTING WITH FUTURE DATE ===")
    test_enrollment_scripts(enrollment_file, future_date)
    test_recruitment_scripts(recruitment_file, future_date)
    test_logic_class(enrollment_file, recruitment_file, future_date)
