import { Grid } from '@material-ui/core';
import { observer } from 'mobx-react';
import React, { FunctionComponent } from 'react';
import { IAssessmentContent, KeyedMap } from 'shared/types';
import ActivityProgress from 'src/components/PatientDetail/ActivityProgress';
import AssessmentProgress from 'src/components/PatientDetail/AssessmentProgress';
import MedicationProgress from 'src/components/PatientDetail/MedicationProgress';
import MoodProgress from 'src/components/PatientDetail/MoodProgress';
import { usePatient, useStores } from 'src/stores/stores';

export const ProgressInformation: FunctionComponent = observer(() => {
    const {
        appConfig: { assessments },
    } = useStores();

    const currentPatient = usePatient();

    const validAssessments = assessments.reduce(
        (prev, curr) => ({ ...prev, [curr.id]: curr }),
        {}
    ) as KeyedMap<IAssessmentContent>;
    const validAssessmentIds = Object.keys(validAssessments);

    const getProgress = (assessmentId: string) => {
        const assessmentContent = validAssessments[assessmentId];
        const assessmentMax = Math.max(...assessmentContent.options.map((o) => o.value));
        const assessment = currentPatient?.assessments.find((a) => a.assessmentId == assessmentId);

        const assessmentLogs = currentPatient?.assessmentLogs.filter((l) => l.assessmentId == assessmentId);

        if (!!assessment) {
            switch (assessmentId) {
                case 'phq-9':
                case 'gad-7':
                    return (
                        <Grid item xs={12} sm={12} key={assessmentId}>
                            <AssessmentProgress
                                assessment={assessment}
                                assessmentLogs={assessmentLogs}
                                instruction={assessmentContent.instruction}
                                questions={assessmentContent.questions}
                                options={assessmentContent.options}
                                maxValue={assessmentMax}
                                canAdd={true}
                            />
                        </Grid>
                    );
                case 'medication':
                    return (
                        <Grid item xs={12} sm={12} key={assessmentId}>
                            <MedicationProgress assessment={assessment} assessmentLogs={assessmentLogs} />
                        </Grid>
                    );
                case 'mood':
                    return (
                        <Grid item xs={12} sm={12} key={assessmentId}>
                            <MoodProgress
                                assessment={assessment}
                                maxValue={assessmentMax}
                                moodLogs={currentPatient?.moodLogs || []}
                            />
                        </Grid>
                    );
            }
        }
    };

    return (
        <Grid container spacing={3} alignItems="stretch" direction="row">
            {validAssessmentIds.map(getProgress)}
            <Grid item xs={12} sm={12}>
                <ActivityProgress />
            </Grid>
        </Grid>
    );
});

export default ProgressInformation;