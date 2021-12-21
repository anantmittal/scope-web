import { Grid, Typography } from '@material-ui/core';
import { GridColDef } from '@material-ui/x-grid';
import { format } from 'date-fns';
import compareDesc from 'date-fns/compareDesc';
import React, { FunctionComponent } from 'react';
import { IAssessment, IMoodLog } from 'shared/types';
import ActionPanel from 'src/components/common/ActionPanel';
import { AssessmentVis } from 'src/components/common/AssessmentVis';
import { Table } from 'src/components/common/Table';
import { getString } from 'src/services/strings';
import { usePatient } from 'src/stores/stores';

export interface IMoodProgressProps {
    assessment: IAssessment;
    maxValue: number;
    moodLogs: IMoodLog[];
}

export const MoodProgress: FunctionComponent<IMoodProgressProps> = (props) => {
    const currentPatient = usePatient();

    const { moodLogs, assessment, maxValue } = props;

    const sortedMoodLogs = moodLogs?.slice().sort((a, b) => compareDesc(a.recordedDate, b.recordedDate));

    const tableData = sortedMoodLogs?.map((a) => {
        return {
            date: format(a.recordedDate, 'MM/dd/yyyy'),
            rating: a.mood,
            id: a.logId,
            comment: a.comment,
        };
    });

    const columns: GridColDef[] = [
        {
            field: 'date',
            headerName: getString('patient_progress_mood_header_date'),
            width: 100,
            sortable: true,
            hideSortIcons: false,
        },
        {
            field: 'rating',
            headerName: getString('patient_progress_mood_header_mood'),
            width: 80,
            align: 'center',
        },
        {
            field: 'comment',
            headerName: getString('patient_progress_mood_header_comment'),
            width: 200,
            align: 'left',
        },
    ];

    return (
        <ActionPanel
            id={assessment.assessmentId}
            title={assessment.assessmentName}
            loading={currentPatient?.state == 'Pending'}>
            <Grid container spacing={2} alignItems="stretch">
                {!!sortedMoodLogs && sortedMoodLogs.length > 0 && (
                    <Table
                        rows={tableData}
                        columns={columns.map((c) => ({
                            sortable: false,
                            filterable: false,
                            editable: false,
                            hideSortIcons: true,
                            disableColumnMenu: true,
                            ...c,
                        }))}
                        autoPageSize
                        autoHeight={true}
                        isRowSelectable={(_) => false}
                    />
                )}
                {!!sortedMoodLogs && sortedMoodLogs.length > 0 && (
                    <Grid item xs={12}>
                        <AssessmentVis
                            data={sortedMoodLogs.map((log) => ({
                                recordedDate: log.recordedDate,
                                pointValues: { Mood: log.mood },
                            }))}
                            maxValue={maxValue}
                            useTime={true}
                        />
                    </Grid>
                )}
                {(!sortedMoodLogs || sortedMoodLogs.length == 0) && (
                    <Grid item xs={12}>
                        <Typography>{getString('patient_progress_mood_empty')}</Typography>
                    </Grid>
                )}
            </Grid>
        </ActionPanel>
    );
};

export default MoodProgress;