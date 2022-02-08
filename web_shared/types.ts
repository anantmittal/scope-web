import {
    ActivitySuccessType,
    AssessmentFrequency,
    BAChecklistFlags,
    BehavioralStrategyChecklistFlags,
    CancerTreatmentRegimenFlags,
    ClinicCode,
    ContactType,
    DayOfWeek,
    DayOfWeekFlags,
    DepressionTreatmentStatus,
    DiscussionFlags,
    DueType,
    FollowupSchedule,
    OtherSpecify,
    PatientEthnicity,
    PatientGender,
    PatientPronoun,
    PatientRaceFlags,
    PatientSex,
    Referral,
    ReferralStatus,
    SessionType
} from './enums';

export type KeyedMap<T> = { [key: string]: T };

export interface IUser extends IIdentity {
    authToken: string;
}

export interface IIdentity {
    identityId: string;
    name: string;
    // patients, social workers (10 patients but have managers too), consulting psychiatrists, oncologists (probably won't access regisrty)
}

export interface IReferralStatus {
    referralType: Referral | OtherSpecify;
    referralStatus: ReferralStatus;
    referralOther?: string; // If the referralType is Other, then provide the detail in this field
}

export type ISessionOrCaseReview = ISession | ICaseReview;

export interface ISession {
    sessionId: string;
    date: Date;
    sessionType: SessionType;
    billableMinutes: number;

    // Medications
    medicationChange: string;
    currentMedications: string;

    // Behavioral strategies
    behavioralStrategyChecklist: BehavioralStrategyChecklistFlags;
    behavioralStrategyOther: string;
    behavioralActivationChecklist: BAChecklistFlags;

    // Referrals -
    referrals: IReferralStatus[];

    otherRecommendations: string;
    sessionNote: string;
}

export interface ICaseReview {
    reviewId: string;
    date: Date;
    consultingPsychiatrist: IIdentity;

    medicationChange: string;
    behavioralStrategyChange: string;
    referralsChange: string;

    otherRecommendations: string;
    reviewNote: string;
}

export interface IAssessment {
    assessmentId: string;
    // Category. why is this a string, gad-7, phq-9
    assessmentName: string;
    assigned: boolean;
    assignedDate: Date;
    frequency: AssessmentFrequency;
    dayOfWeek: DayOfWeek;
}

export interface IActivity {
    activityId: string;
    name: string;
    value: string;
    lifeareaId: string;
    startDate: Date;
    timeOfDay: number;
    hasReminder: boolean;
    reminderTimeOfDay: number;
    hasRepetition: boolean;
    repeatDayFlags: DayOfWeekFlags;
    isActive: boolean;
    isDeleted: boolean;
}

export interface IScheduledItem {
    scheduleId: string;
    dueDate: Date;
    dueType: DueType;
}

export interface IScheduledActivity extends IScheduledItem {
    activityId: string;
    activityName: string;
    reminder: Date;

    completed: boolean;
}

export interface IScheduledAssessment extends IScheduledItem {
    assessmentId: string;
    assessmentName: string;

    completed: boolean;
}
export type AssessmentData = KeyedMap<number | undefined>;

export interface ILog {
    logId?: string; // Should these be optional until committed?
    recordedDate: Date;
    comment?: string;
}

export interface IActivityLog extends ILog {
    scheduleId: string;
    activityName: string;

    completed?: boolean;
    success?: ActivitySuccessType;
    alternative?: string;
    pleasure?: number;
    accomplishment?: number;
}

export interface IAssessmentLog extends ILog {
    scheduleId: string;
    assessmentId: string; // NEW
    assessmentName: string;

    completed: boolean;
    patientSubmitted?: boolean; // NEW
    submittedBy?: IIdentity;
    pointValues: AssessmentData;
    totalScore?: number;
}

export interface IMoodLog extends ILog {
    mood: number;
}

export interface IPatientProfile {
    name: string;
    MRN: string;
    clinicCode?: ClinicCode;
    birthdate?: Date;
    sex?: PatientSex;
    gender?: PatientGender;
    pronoun?: PatientPronoun;
    race?: PatientRaceFlags;
    ethnicity?: PatientEthnicity;
    primaryOncologyProvider?: IIdentity;
    primaryCareManager?: IIdentity;
    discussionFlag?: DiscussionFlags;
    followupSchedule?: FollowupSchedule;
    depressionTreatmentStatus?: DepressionTreatmentStatus;
}

export interface IClinicalHistory {
    primaryCancerDiagnosis?: string;
    // Date is a string to allow flexibility for social worker.
    // This particulate date is never used for any computations.
    dateOfCancerDiagnosis?: string;
    currentTreatmentRegimen?: CancerTreatmentRegimenFlags;
    currentTreatmentRegimenOther?: string;
    currentTreatmentRegimenNotes?: string;
    psychDiagnosis?: string;
    pastPsychHistory?: string;
    pastSubstanceUse?: string;
    psychSocialBackground?: string;
}

export interface IContact {
    contactType: ContactType;
    name: string;
    address?: string;
    phoneNumber?: string;
    emergencyNumber?: string;
}

export interface ISafetyPlan {
    assigned: boolean;
    assignedDate: Date;
    lastUpdatedDate?: Date;
    reasonsForLiving?: string;
    warningSigns?: string[];
    copingStrategies?: string[];
    // contacts are unique for a patient.
    distractions?: (string | IContact)[];
    supporters?: IContact[];
    professionalSupporters?: IContact[];
    urgentServices?: IContact[];
    safeEnvironment?: string[];
}

export interface IValuesInventory {


    // registry toggle. everything except
    assigned: boolean;
    assignedDate: Date;
    lastUpdatedDate?: Date;

    // Length 5
    values?: ILifeAreaValue[];
}

export interface ILifeAreaContent {
    id: string;
    name: string;
    examples: ILifeAreaValue[];
}

export interface ILifeAreaValue {
    //
    id: string; // unique identifier.
    // value patient created
    name: string;
    dateCreated: Date;
    dateEdited: Date;
    // identifier ties it back to life areas.
    lifeareaId: string; // educaiton, mindobody, etc.
    activities: ILifeAreaValueActivity[];
}

export interface ILifeAreaValueActivity {
    id: string;
    name: string;
    // going to point towards id in ILifeAreaValue
    valueId: string;
    dateCreated: Date;
    dateEdited: Date;
    // could be skipped. it's goung to be exactly same as lifeareaId in ILifeAreaValue
    lifeareaId: string;
    enjoyment?: number;
    importance?: number;
}

export interface IPatient {
    identity: IIdentity;

    // Patient info - registry only
    profile: IPatientProfile;
    clinicalHistory: IClinicalHistory;

    // Values inventory and safety plan - patient only
    valuesInventory: IValuesInventory;
    safetyPlan: ISafetyPlan;

    // Sessions - registry only
    sessions: ISession[];
    caseReviews: ICaseReview[];

    // Assessments - filled by patient but scheduled might be regsitry

    // check if ypte to capture assessments exist - phq9, and gad7.

    assessments: IAssessment[];
    scheduledAssessments: IScheduledAssessment[];
    assessmentLogs: IAssessmentLog[];

    // Activities - filled by patient
    activities: IActivity[];
    scheduledActivities: IScheduledActivity[];
    activityLogs: IActivityLog[];

    // Mood logs - filled by patient.
    // medication tracking similar to moodlogs.
    // Missing something. medication tracking.
    /*
    boolean value to say if you have takedn the medication.
    boolean question for care team.
    question if above is yes. date. maybe use ILog?
    */
    moodLogs: IMoodLog[];
}

export interface IPatientList {
    patients: IPatient[];
}

export interface IAppConfig {
    assessments: IAssessmentContent[];
    lifeAreas: ILifeAreaContent[];
    resources: IResourceContent[];
}

export interface IAssessmentContent {
    id: string;
    name: string;
    instruction: string;
    questions: { question: string; id: string }[];
    options: { text: string; value: number }[];
}

export interface IResourceContent {
    id: string;
    name: string;
    resources: IResourceItem[];
}

export interface IResourceItem {
    name: string;
    filename: string;
}

export interface IPatientConfig {
    assignedValuesInventory: boolean;
    assignedSafetyPlan: boolean;
    assignedAssessmentIds: string[];
}

export interface IAppConfig {
    assessments: IAssessmentContent[];
    lifeAreas: ILifeAreaContent[];
    resources: IResourceContent[];
}

export interface IAssessmentContent {
    id: string;
    name: string;
    instruction: string;
    questions: { question: string; id: string }[];
    options: { text: string; value: number }[];
    interpretationName: string;
    interpretationTable: { score: string; max: number; interpretation: string }[];
}

export interface ILifeAreaContent {
    id: string;
    name: string;
    examples: ILifeAreaValue[];
}

export interface IResourceContent {
    name: string;
    resources: IResourceItem[];
}

export interface IResourceItem {
    name: string;
    filename: string;
}

// Removed for merge on 2/5
//
// export interface IStoredDocument {
//     _id: string;
//     _type: string;
//     _set_id?: string;
//     _rev: number;
// }

export const isSession = (session: ISession | ICaseReview): session is ISession => {
    return (session as ISession)?.sessionId !== undefined;
};
