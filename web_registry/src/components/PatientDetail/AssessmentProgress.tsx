import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    Typography,
    withTheme,
} from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';
import AssignmentIcon from '@material-ui/icons/Assignment';
import AssignmentTurnedInIcon from '@material-ui/icons/AssignmentTurnedIn';
import SettingsIcon from '@material-ui/icons/Settings';
import { GridCellParams, GridColDef, GridRowParams } from '@material-ui/x-grid';
import { compareAsc, format } from 'date-fns';
import compareDesc from 'date-fns/compareDesc';
import { action } from 'mobx';
import { observer, useLocalObservable } from 'mobx-react';
import React, { FunctionComponent } from 'react';
import { AssessmentFrequency, assessmentFrequencyValues, DayOfWeek, daysOfWeekValues } from 'shared/enums';
import { AssessmentData, IAssessment, IAssessmentLog, IIdentity } from 'shared/types';
import ActionPanel, { IActionButton } from 'src/components/common/ActionPanel';
import { AssessmentVis } from 'src/components/common/AssessmentVis';
import { GridDropdownField } from 'src/components/common/GridField';
import Questionnaire from 'src/components/common/Questionnaire';
import { Table } from 'src/components/common/Table';
import { getString } from 'src/services/strings';
import { usePatient, useStores } from 'src/stores/stores';
import { getAssessmentScore, getAssessmentScoreColorName } from 'src/utils/assessment';
import styled from 'styled-components';

const ScoreCell = withTheme(
    styled.div<{ score: number; assessmentId: string }>((props) => ({
        width: 'calc(100% + 16px)',
        marginLeft: -8,
        marginRight: -8,
        padding: props.theme.spacing(1),
        backgroundColor:
            props.theme.customPalette.scoreColors[getAssessmentScoreColorName(props.assessmentId, props.score)],
    }))
);

export interface IAssessmentProgressProps {
    instruction?: string;
    questions: { question: string; id: string }[];
    options: { text: string; value: number }[];
    maxValue: number;
    assessment: IAssessment;
    assessmentLogs: IAssessmentLog[];
    canAdd?: boolean;
    useTime?: boolean;
}

export const AssessmentProgress: FunctionComponent<IAssessmentProgressProps> = observer((props) => {
    const { currentUserIdentity } = useStores();
    const currentPatient = usePatient();

    const { instruction, questions, options, assessment, assessmentLogs, maxValue, canAdd, useTime } = props;

    const configureState = useLocalObservable<{
        openConfigure: boolean;
        frequency: AssessmentFrequency;
        dayOfWeek: DayOfWeek;
    }>(() => ({
        openConfigure: false,
        frequency: 'Every 2 weeks',
        dayOfWeek: 'Monday',
    }));

    const logState = useLocalObservable<{
        openEdit: boolean;
        totalOnly: boolean;
        scheduleId: string;
        logId: string;
        recordedDate: Date;
        pointValues: AssessmentData;
        totalScore: number;
        comment: string;
        patientSubmitted: boolean;
    }>(() => ({
        openEdit: false,
        totalOnly: false,
        scheduleId: '',
        logId: '',
        recordedDate: new Date(),
        comment: '',
        pointValues: {},
        totalScore: -1,
        patientSubmitted: false,
    }));

    const handleClose = action(() => {
        logState.openEdit = false;
        configureState.openConfigure = false;
    });

    const handleAddRecord = action(() => {
        logState.totalOnly = false;

        logState.scheduleId = '';
        logState.logId = '';
        logState.comment = '';
        logState.pointValues = {};
        logState.totalScore = -1;
    });

    const handleConfigure = action(() => {
        configureState.openConfigure = true;
        configureState.frequency = assessment.frequency || 'None';
        configureState.dayOfWeek = assessment.dayOfWeek || 'Monday';
    });

    const onSaveEditRecord = action(() => {
        const { scheduleId, logId, recordedDate, comment, pointValues, totalScore } = logState;

        if (!!logId) {
            currentPatient.updateAssessmentLog({
                logId,
                recordedDate,
                comment,

                scheduleId,
                assessmentId: assessment.assessmentId,
                assessmentName: assessment.assessmentName,
                completed: true,
                patientSubmitted: false,
                submittedBy: currentUserIdentity as IIdentity,
                pointValues,
                totalScore,
            });
        } else {
            currentPatient.addAssessmentLog({
                logId: '',
                recordedDate,
                comment,

                scheduleId: 'on-demand',
                assessmentId: assessment.assessmentId,
                assessmentName: assessment.assessmentName,
                completed: true,
                patientSubmitted: false,
                submittedBy: currentUserIdentity as IIdentity,
                pointValues,
                totalScore,
            });
        }
        logState.openEdit = false;
    });

    const onSaveConfigure = action(() => {
        const { frequency, dayOfWeek } = configureState;
        var newAssessment = { ...assessment } as Partial<IAssessment>;
        newAssessment.frequency = frequency;
        newAssessment.dayOfWeek = dayOfWeek;
        currentPatient.updateAssessment(newAssessment);
        configureState.openConfigure = false;
    });

    const onQuestionSelect = action((qid: string, value: number) => {
        logState.pointValues[qid] = value;
    });

    const onDateChange = action((date: Date) => {
        logState.recordedDate = date;
    });

    const onTotalChange = action((value: number) => {
        logState.totalScore = value;
    });

    const onToggleTotalOnly = action((value: boolean) => {
        logState.totalOnly = value;
    });

    const onFrequencyChange = action((freq: AssessmentFrequency) => {
        configureState.frequency = freq;
    });

    const onDayOfWeekChange = action((dow: DayOfWeek) => {
        configureState.dayOfWeek = dow;
    });

    const onCommentChange = action((comment: string) => {
        logState.comment = comment;
    });

    const selectedValues = questions.map((q) => logState.pointValues[q.id]);
    const saveDisabled = logState.totalOnly
        ? logState.totalScore == undefined
        : selectedValues.findIndex((v) => v == undefined) >= 0;

    const questionIds = questions.map((q) => q.id);

    const tableData = assessmentLogs
        .slice()
        .sort((a, b) => compareDesc(a.recordedDate, b.recordedDate))
        .map((a) => {
            return {
                date: format(a.recordedDate, 'MM/dd/yyyy'),
                total: getAssessmentScore(a.pointValues) || a.totalScore,
                id: a.logId,
                ...a.pointValues,
                comment: a.comment,
            };
        });

    const recurrence = assessment.assigned
        ? `${assessment.frequency} on ${assessment.dayOfWeek}s, assigned on ${format(
              assessment.assignedDate,
              'MM/dd/yyyy'
          )}`
        : 'Not assigned';

    const renderScoreCell = (props: GridCellParams) => (
        <ScoreCell score={props.value as number} assessmentType={assessment?.assessmentId}>
            {props.value}
        </ScoreCell>
    );
    const columns: GridColDef[] = [
        {
            field: 'date',
            headerName: 'Date',
            width: 100,
            sortable: true,
            hideSortIcons: false,
        },
        {
            field: 'total',
            headerName: 'Total',
            width: 80,
            renderCell: renderScoreCell,
            align: 'center',
        },
        ...questionIds.map(
            (q) =>
                ({
                    field: q,
                    headerName: q,
                    width: 80,
                    align: 'center',
                } as GridColDef)
        ),
        {
            field: 'comment',
            headerName: 'Comment',
            width: 120,
        },
    ];

    const onRowClick = action((param: GridRowParams) => {
        const id = param.getValue(param.id, 'id') as string;
        const data = assessmentLogs.find((a) => a.logId == id);

        if (!!data) {
            logState.openEdit = true;
            logState.totalOnly = !!data.totalScore && data.totalScore >= 0;
            logState.scheduleId = data.scheduleId;
            logState.logId = data.logId || '';
            logState.recordedDate = data.recordedDate;
            Object.assign(logState.pointValues, data.pointValues);
            logState.totalScore = data.totalScore || -1;
            logState.comment = data.comment || '';
        }
    });

    return (
        <ActionPanel
            id={assessment.assessmentId}
            title={assessment.assessmentName}
            inlineTitle={recurrence}
            loading={currentPatient?.state == 'Pending'}
            actionButtons={[
                {
                    icon: assessment.assigned ? <AssignmentTurnedInIcon /> : <AssignmentIcon />,
                    text: assessment.assigned
                        ? getString('patient_progress_assessment_assigned_button')
                        : getString('patient_progress_assessment_assign_button'),
                    onClick: assessment.assigned
                        ? undefined
                        : () => currentPatient?.assignAssessment(assessment.assessmentId),
                } as IActionButton,
            ]
                .concat(
                    assessment.assigned
                        ? [
                              {
                                  icon: <SettingsIcon />,
                                  text: getString('patient_progress_assessment_action_configure'),
                                  onClick: handleConfigure,
                              } as IActionButton,
                          ]
                        : []
                )
                .concat(
                    canAdd
                        ? [
                              {
                                  icon: <AddIcon />,
                                  text: getString('patient_progress_assessment_action_add'),
                                  onClick: handleAddRecord,
                              } as IActionButton,
                          ]
                        : []
                )}>
            <Grid container spacing={2} alignItems="stretch">
                {assessment.assessmentId != 'mood' && assessmentLogs.length > 0 && (
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
                        onRowClick={onRowClick}
                        autoHeight={true}
                        isRowSelectable={(_) => false}
                    />
                )}
                {assessmentLogs.length > 0 && (
                    <Grid item xs={12}>
                        <AssessmentVis
                            data={assessmentLogs.slice().sort((a, b) => compareAsc(a.recordedDate, b.recordedDate))}
                            maxValue={maxValue}
                            useTime={useTime}
                        />
                    </Grid>
                )}
                {assessmentLogs.length == 0 && (
                    <Grid item xs={12}>
                        <Typography>{`There are no ${assessment.assessmentName} scores submitted for this patient`}</Typography>
                    </Grid>
                )}
            </Grid>

            <Dialog open={logState.openEdit} onClose={handleClose} fullWidth maxWidth="lg">
                <DialogTitle>
                    {logState.patientSubmitted
                        ? `Patient submitted ${assessment.assessmentName} record`
                        : !!logState.logId
                        ? `Edit ${assessment.assessmentName} record`
                        : `Add ${assessment.assessmentName} record`}
                </DialogTitle>
                <DialogContent>
                    <Questionnaire
                        readonly={logState.patientSubmitted}
                        questions={questions}
                        options={options}
                        selectedValues={selectedValues}
                        selectedDate={logState.recordedDate}
                        instruction={instruction}
                        onSelect={onQuestionSelect}
                        onDateChange={onDateChange}
                        onTotalChange={onTotalChange}
                        onToggleTotalOnly={onToggleTotalOnly}
                        totalOnly={logState.totalOnly}
                        totalScore={logState.totalScore}
                        comment={logState.comment}
                        onCommentChange={onCommentChange}
                    />
                </DialogContent>
                {logState.patientSubmitted ? (
                    <DialogActions>
                        <Button onClick={handleClose} color="primary">
                            {getString('patient_progress_assessment_dialog_close_button')}
                        </Button>
                    </DialogActions>
                ) : (
                    <DialogActions>
                        <Button onClick={handleClose} color="primary">
                            {getString('patient_progress_assessment_dialog_cancel_button')}
                        </Button>
                        <Button onClick={onSaveEditRecord} color="primary" disabled={saveDisabled}>
                            {getString('patient_progress_assessment_dialog_save_button')}
                        </Button>
                    </DialogActions>
                )}
            </Dialog>
            <Dialog open={configureState.openConfigure} onClose={handleClose}>
                <DialogTitle>{getString('patient_progress_assessment_dialog_configure_title')}</DialogTitle>
                <DialogContent>
                    <Grid container spacing={2} alignItems="stretch">
                        <GridDropdownField
                            editable={true}
                            label={getString('patient_progress_assessment_dialog_configure_frequency_label')}
                            value={configureState.frequency}
                            options={assessmentFrequencyValues}
                            xs={12}
                            sm={12}
                            onChange={(text) => onFrequencyChange(text as AssessmentFrequency)}
                        />
                        <GridDropdownField
                            editable={true}
                            label={getString('patient_progress_assessment_dialog_configure_dayofweek_label')}
                            value={configureState.dayOfWeek}
                            options={daysOfWeekValues}
                            xs={12}
                            sm={12}
                            onChange={(text) => onDayOfWeekChange(text as DayOfWeek)}
                        />
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        {getString('dialog_action_cancel')}
                    </Button>
                    <Button onClick={onSaveConfigure} color="primary">
                        {getString('dialog_action_save')}
                    </Button>
                </DialogActions>
            </Dialog>
        </ActionPanel>
    );
});

export default AssessmentProgress;