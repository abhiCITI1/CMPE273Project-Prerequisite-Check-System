import json
import re

def checkEligibility(applicationType):
    file = open('sampleExtractedText.txt', 'r')
    extractedString = file.read()
    lstTranscriptLines = extractedString.splitlines()
    #print 'lstTranscriptLines= ', lstTranscriptLines
    #print ' # of lines in transcripts= ', len(lstTranscriptLines)
    if(applicationType!='' and applicationType == "Masters"):
        eligible=checkMastersEligibility(lstTranscriptLines);
        print "MASTERs eligibility satisfied= ",eligible
    elif(applicationType!='' and applicationType == "Subject Enrollment"):
        eligible=checkSubEnrollmentEligibility(lstTranscriptLines);
        print "Subject Enrollment eligibility satisfied= ",eligible

def checkMastersEligibility(lstTranscriptLines):
    # Read the conditions file
    with open('mastersApplicationConditions.json') as data_file:
        conditionsData = json.load(data_file)
    print 'conditions data = ', conditionsData

    # Get data from extracted transcript string
    overallConditionSatisfied = 'true'
    for line in lstTranscriptLines:
        if line.lower().strip().find('university') > -1:
            university = line.strip()
            #print '******university found ', university

        if(conditionsData['minGPA']!=''):
            overallConditionSatisfied = 'false'
            if line.lower().strip().find('semester credits') > -1:
                var = line.partition('Semester Credits')[2]
                # print" var = ", var
                if var.lower().find('gpa') > 0:
                    finalGPA = var.partition('GPA')[2]
                    finalGPA = re.findall(r"(\d+\.\d+)", finalGPA)[0]
                    #print '********finalGPA= ', finalGPA
                    finalCredits = var.partition('GPA')[0]
                    finalCredits = finalCredits.strip()
                    finalCredits = re.findall(r"(\d+\.\d+)", finalCredits)[0]
                    #print '*****finalCredits= ', finalCredits
                    if(float(finalGPA) >= float(conditionsData['minGPA'])):
                        overallConditionSatisfied = 'true'
    print "Overall GPA conditions satisfied = ",overallConditionSatisfied

    if(overallConditionSatisfied == "true"):
         # Get the subject conditions for student
        subjectConditions = conditionsData['subjects']
        #print 'conditions data of subjects = ', subjectConditions

        # Check if student satisfies subject conditions
        subjectConditionSatisfied = 'true'
        if subjectConditions != '':
            #subjectConditionSatisfied = 'false'
            for i in range(0, len(subjectConditions)):
                #If subject condition fails for any subject,skip checking conditions for other subjects
                if i != 0 and subjectConditionSatisfied != 'true':
                    break
                #print '***checking conditions for subject=', subjectConditions[i]['name']
                # Reinitialize subjectConditionsSatisfied boolean for each subject
                subjectConditionSatisfied = 'false'

                for line in lstTranscriptLines:
                    # Check if line contains the subject
                    if line.lower().strip().find(subjectConditions[i]['name'].lower()) > -1:
                        # If required, check the credits in this subject
                        if(subjectConditions[i]['mincredits'] != ""):
                            # Find floting number
                            credits = re.findall(r"(\d+\.\d+)", line)[0]
                            #print '****credtis in subject ', \
                            #    subjectConditions[i]['name'], 'are', float(credits)
                            if(float(credits)!='' and float(credits)!='undefined' and float(credits) >= float(subjectConditions[i]['mincredits'])):
                                subjectConditionSatisfied = 'true'
                        else:
                            subjectConditionSatisfied = 'true'
                #print "***Conditions satisfied for subject= ", subjectConditionSatisfied
            print "All Subject conditions satisfied= ", subjectConditionSatisfied
            if(subjectConditionSatisfied == 'true'):
                return "true"
    else: #Overall conditions not satisfied
        return "false"

def checkSubEnrollmentEligibility(lstTranscriptLines):
    # Read the conditions file
    with open('subjectEnrollmentConditions.json') as data_file:
        conditionsData = json.load(data_file)
    print 'conditions data = ', conditionsData

if __name__ == '__main__':
    applicationType = "Subject Enrollment"
    checkEligibility(applicationType)
