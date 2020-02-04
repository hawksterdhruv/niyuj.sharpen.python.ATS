# Table Names

## Job_Positions

    JobId				String/Number           Primary key
    Skills 				String
    Experience 			Number
    No of Positions		Number
    Title				String
    Status				String                  open/closed/hold
    Grade				String
    ProjectId			Number

## Project

    ProjectId 			Number                  Primary key
    Name				String

## Interview Details

    InterviewId         Number                  Primary Key
    Date				DateTime
    Location			String
    EmployeeId		    EmployeeName		    (Referred from Interview Panel))
    Feedback			String
    RoundName/Type	    String
    Channel             String
    RoundResult			String/Boolean
    JobHasCandidateId	String/Number		    (Referred from Job_Positions)
    Project id 			Number
    Hiring Manager   	String

## Candidate

    CandidateId			Number		            Primary key
    Name				String
    Skills				String
    Experience			Number
    EmailId				string
    Address				String
    MobileNo			Number
    Source				String                  (referral, direct, Job portal..)
    ReferredBy			String/Number 	        (try to fetch from existing employee table)
    Status				String 		            shortlisted/Rejected/Selected etc.
    JobId				String/Number	        (Referred from Job_Positions table)
    PanCard				String			        Unique Not Null
    Resume 				String(File)
    Current CTC 		Number
    Expected CTC 		Number
    Current Org         String
    Notice Period		Number

## Job_has_candidate table

    JobHasCandidateId   Number                  Primary Key
    JobId               Number
    CandidateId         Number
