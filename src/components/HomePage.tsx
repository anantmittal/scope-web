import Typography from '@material-ui/core/Typography';
import { observer } from 'mobx-react';
import React, { FunctionComponent } from 'react';
import { useStores } from '../stores/stores';
import { getTodayString } from '../utils/formatter';
import { PageHeaderContainer, PageHeaderSubtitle, PageHeaderTitle } from './common/PageHeader';

export const HomePage: FunctionComponent = observer(() => {
    const rootStore = useStores();
    return (
        <div>
            <PageHeaderContainer>
                <PageHeaderTitle>{`Welcome ${rootStore.userStore.name}`}</PageHeaderTitle>
                <PageHeaderSubtitle>{`${getTodayString()}`}</PageHeaderSubtitle>
            </PageHeaderContainer>
            <Typography paragraph>
                123 This is home. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
                incididunt ut labore et dolore magna aliqua. Rhoncus dolor purus non enim praesent elementum facilisis
                leo vel. Risus at ultrices mi tempus imperdiet. Semper risus in hendrerit gravida rutrum quisque non
                tellus. Convallis convallis tellus id interdum velit laoreet id donec ultrices. Odio morbi quis commodo
                odio aenean sed adipiscing. Amet nisl suscipit adipiscing bibendum est ultricies integer quis. Cursus
                euismod quis viverra nibh cras. Metus vulputate eu scelerisque felis imperdiet proin fermentum leo.
                Mauris commodo quis imperdiet massa tincidunt. Cras tincidunt lobortis feugiat vivamus at augue. At
                augue eget arcu dictum varius duis at consectetur lorem. Velit sed ullamcorper morbi tincidunt. Lorem
                donec massa sapien faucibus et molestie ac.
            </Typography>
        </div>
    );
});

export default HomePage;
