from datetime import date, datetime, timedelta

import numpy as np
from lorem.text import TextLorem

from assessments import gad7Assessment, moodAssessment, phq9Assessment
from enums import (
    AssessmentFrequency,
    AssessmentType,
    BehavioralActivationChecklist,
    CancerTreatmentRegimen,
    ClinicCode,
    DepressionTreatmentStatus,
    DiscussionFlag,
    FollowupSchedule,
    PatientSex,
    Referral,
    SessionType,
    TreatmentChange,
    TreatmentPlan,
)

lorem = TextLorem(srange=(4, 16), prange=(4, 8))
shortLorem = TextLorem(srange=(4, 8), prange=(1, 3))

firstNames = [
    "Paisley",
    "Vince",
    "Prudence",
    "Floyd",
    "Marty",
    "Yvonne",
    "Russ",
    "Herb",
    "Hannah",
    "Melanie",
    "Dwayne",
    "Clifford",
    "Garth",
    "Rachel",
    "Phoebe",
    "Doug",
    "Mortimer",
    "Heath",
    "Iris",
    "Tony",
]

lastNames = [
    "Lowe",
    "Dawson",
    "Porter",
    "Tomlinson",
    "Windrow",
    "Cook",
    "Wolfe",
    "Chapman",
    "Malone",
    "Green",
    "Fairbank",
    "Wood",
    "Miller",
    "Clayton",
    "Russell",
    "Atkinson",
    "Whitehead",
    "Greene",
    "Cannon",
    "Pope",
]

careManagers = ["Luke Skywalker", "Leia Organa", "Han Solo", "Padme Amidala"]


def getRandomFakePatients():
    return [getFakePatient() for idx in range(getRandomInteger(3, 10))]


def getFakePatient():
    return {
        # Medical information
        "MRN": getRandomInteger(10000, 1000000),
        "firstName": getRandomItem(firstNames),
        "lastName": getRandomItem(lastNames),
        "birthdate": datetime(
            getRandomInteger(1930, 2000),
            getRandomInteger(1, 13),
            getRandomInteger(1, 28),
        ),
        "sex": getRandomItem(PatientSex).value,
        "clinicCode": getRandomItem(ClinicCode).value,
        # Clinical history
        "primaryCancerDiagnosis": shortLorem.paragraph(),
        "pastPsychHistory": shortLorem.paragraph(),
        "pastSubstanceUse": shortLorem.paragraph(),
        # Treatment information
        "primaryCareManager": getRandomItem(careManagers),
        "currentTreatmentRegimen": getRandomFlags(CancerTreatmentRegimen),
        "currentTreatmentRegimenOther": shortLorem.sentence(),
        "depressionTreatmentStatus": getRandomItem(DepressionTreatmentStatus).value,
        "psychDiagnosis": shortLorem.paragraph(),
        "discussionFlag": getRandomFlags(DiscussionFlag),
        "followupSchedule": getRandomItem(FollowupSchedule).value,
        # TBD
        "referral": getRandomItem(Referral).value,
        "treatmentPlan": shortLorem.paragraph(),
        "psychHistory": shortLorem.paragraph(),
        "substanceUse": shortLorem.paragraph(),
        "psychMedications": shortLorem.paragraph(),
        "psychDiagnosis": shortLorem.paragraph(),
        # Sessions
        "sessions": getFakeSessions(),
        # Assessments
        "assessments": getFakeAssessments(),
        # Activities
        "activities": getFakeActivities(),
    }


def getRandomInteger(minInclusive, maxExclusive):
    return int(np.random.randint(low=minInclusive, high=maxExclusive))


def getRandomItem(enum):
    return np.random.choice(enum, 1)[0]


def getRandomBoolean():
    return np.random.randint(0, 2) == 0


def sample(enum, count):
    return np.random.choice(enum, count, replace=False)


def getRandomFlags(enum):
    flags = dict()
    for key in enum:
        flags[key.value] = getRandomBoolean()

    return flags


def getFakeAssessments():
    return [
        {
            "assessmentId": a.value,
            "assessmentType": a.value,
            "frequency": getRandomItem(AssessmentFrequency).value,
            "data": getAssessmentDataPoints(a.value),
        }
        for a in sample(AssessmentType, getRandomInteger(1, 3))
    ]


def getFakeAssessmentDataPoint(assessmentType):
    points = dict()
    if assessmentType == "PHQ-9":
        for q in phq9Assessment.get("questions", []):
            points[q["id"]] = getRandomInteger(0, 4)
        return points
    elif assessmentType == "GAD-7":
        for q in gad7Assessment.get("questions", []):
            points[q["id"]] = getRandomInteger(0, 4)
        return points
    else:
        return {"Mood": getRandomInteger(1, 6)}


def getAssessmentDataPoints(assessmentType):
    return [
        {
            "assessmentDataId": "%s-%d" % (assessmentType, idx),
            "assessmentType": assessmentType,
            "date": datetime.now()
            - timedelta(days=getRandomInteger(0, 3) + idx * getRandomInteger(5, 8)),
            "pointValues": getFakeAssessmentDataPoint(assessmentType),
            "comment": shortLorem.paragraph(),
        }
        for idx in range(getRandomInteger(5, 10))
    ]


def getFakeSessions():
    sessionCount = getRandomInteger(1, 10)
    return [
        {
            "sessionId": "Initial assessment" if idx == 0 else "session-%d" % idx,
            "date": datetime.now()
            - timedelta(
                days=getRandomInteger(-2, 2)
                + (sessionCount - idx) * getRandomInteger(13, 18)
            ),
            "sessionType": getRandomItem(SessionType).value,
            "billableMinutes": int(getRandomItem([30, 45, 60, 80])),
            "treatmentPlan": getRandomItem(TreatmentPlan).value,
            "treatmentChange": getRandomItem(TreatmentChange).value,
            "behavioralActivationChecklist": getRandomFlags(
                BehavioralActivationChecklist
            ),
            "sessionNote": lorem.paragraph(),
        }
        for idx in range(sessionCount)
    ]


def getFakeActivities():
    return [
        {
            "activityId": "%s" % idx,
            "activityName": shortLorem.sentence(),
            "moodData": getAssessmentDataPoints("Mood Logging"),
        }
        for idx in range(getRandomInteger(1, 3))
    ]
