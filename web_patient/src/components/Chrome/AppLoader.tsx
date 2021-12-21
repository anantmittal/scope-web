import { Box, CircularProgress, Fade, Paper, Typography } from '@material-ui/core';
import zIndex from '@material-ui/core/styles/zIndex';
import React, { FunctionComponent } from 'react';
import styled from 'styled-components';

const Cover = styled(Fade)({
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    background: 'white',
    zIndex: zIndex.modal + 1,
});

export interface IAppLoaderProps {
    isLoading: boolean;
    text: string;
}

export const AppLoader: FunctionComponent<IAppLoaderProps> = (props) => {
    const { isLoading, text } = props;

    return (
        <Cover
            in={isLoading}
            style={{
                transitionDelay: !isLoading ? '800ms' : '0ms',
            }}
            unmountOnExit>
            <Paper elevation={0} square>
                <Box
                    top={0}
                    left={0}
                    bottom={0}
                    right={0}
                    position="absolute"
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    flexDirection="column">
                    <CircularProgress />
                    <Typography variant="caption" component="div" color="primary">
                        {text}
                    </Typography>
                </Box>
            </Paper>
        </Cover>
    );
};

export default AppLoader;