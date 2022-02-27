import { Box, Button, CircularProgress, Typography, Snackbar } from '@mui/material';
import React, { Fragment, FunctionComponent } from 'react';
import { IPromiseQueryState } from 'shared/promiseQuery';
import styled, { withTheme } from 'styled-components';

const ProgressContainer = withTheme(
    styled.div((props) => ({
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderRadius: props.theme.spacing(4),
        padding: props.theme.spacing(4),
        [props.theme.breakpoints.down('md')]: {
            padding: props.theme.spacing(8),
        },
    })),
);

export const PageLoader: FunctionComponent<{
    state: IPromiseQueryState;
    name: string;
    onRetry?: () => void;
    children: React.ReactNode;
}> = (props) => {
    const { state, name, children, onRetry } = props;

    const retryAction = onRetry && (
        <Button color="secondary" size="small" onClick={onRetry}>
            RETRY
        </Button>
    );

    return (
        <Fragment>
            {state.pending && (
                <ProgressContainer>
                    <CircularProgress />
                    <Box sx={{ height: 40 }} />
                    <Typography>{`Retrieving ${name}...`}</Typography>
                </ProgressContainer>
            )}

            {state.done && <Box sx={{ opacity: state.pending ? 0.5 : 1 }}>{children}</Box>}
            <Snackbar
                open={state.error}
                message={`Sorry, there was an error retrieving ${name}. Please try again.`}
                action={retryAction}
            />
        </Fragment>
    );
};

export default PageLoader;
