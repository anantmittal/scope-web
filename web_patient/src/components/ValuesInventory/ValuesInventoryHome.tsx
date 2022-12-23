import { Divider, List, ListItem, ListItemIcon, ListItemText, Typography } from '@mui/material';
import { styled } from '@mui/styles';
import { action } from 'mobx';
import { observer } from 'mobx-react';
import React, { Fragment, FunctionComponent } from 'react';
import { useNavigate } from 'react-router';
import { Link } from 'react-router-dom';
import ContentLoader from 'src/components/Chrome/ContentLoader';
import DetailPage from 'src/components/common/DetailPage';
import { getActivitiesCountString, getLifeAreaIcon, getValuesCountString } from 'src/components/ValuesInventory/values';
import { getString } from 'src/services/strings';
import { useStores } from 'src/stores/stores';
import { LifeAreaIdOther } from 'shared/enums';

const InstructionText = styled(Typography)({
    lineHeight: 1,
});

export const ValuesInventoryHome: FunctionComponent = observer(() => {
    const rootStore = useStores();
    const { lifeAreas } = rootStore.appContentConfig;
    const navigate = useNavigate();
    const { patientStore } = rootStore;

    const handleGoBack = action(() => {
        navigate(-1);
    });

    return (
        <DetailPage title={getString('values_inventory_home_title')} onBack={handleGoBack}>
            <InstructionText paragraph>{getString('values_inventory_home_instruction1')}</InstructionText>
            <InstructionText paragraph>{getString('values_inventory_home_instruction2')}</InstructionText>
            <InstructionText paragraph>{getString('values_inventory_home_instruction3')}</InstructionText>
            <InstructionText paragraph>{getString('values_inventory_home_instruction4')}</InstructionText>
            <ContentLoader
                state={patientStore.loadValuesInventoryState}
                name="values & activities inventory"
                onRetry={() => patientStore.loadValuesInventory()}>
                <List>
                    {lifeAreas.map((la, idx) => {
                        const lifeAreaActivities = patientStore.getActivitiesByLifeAreaId(la.id);
                        const lifeAreaValues = patientStore.getValuesByLifeAreaId(la.id);

                        return (
                            <Fragment key={la.id}>
                                <ListItem disableGutters button component={Link} to={`${la.id}`}>
                                    <ListItemIcon>{getLifeAreaIcon(la.id)}</ListItemIcon>
                                    <ListItemText
                                        primary={la.name}
                                        secondary={
                                            getValuesCountString(lifeAreaValues.length) +
                                            '; ' +
                                            getActivitiesCountString(lifeAreaActivities.length)
                                        }
                                    />
                                </ListItem>
                                {idx < lifeAreas.length - 1 && <Divider variant="middle" />}
                            </Fragment>
                        );
                    })}
                    {(() => {
                        const otherActivities = patientStore.getActivitiesWithoutValueId();

                        return !!otherActivities && (
                            <Fragment>
                                <Divider variant="middle" />
                                <ListItem disableGutters button component={Link} to={LifeAreaIdOther}>
                                    <ListItemIcon>{getLifeAreaIcon(LifeAreaIdOther)}</ListItemIcon>
                                    <ListItemText
                                        primary={getString('values_inventory_home_other_activities')}
                                        secondary={getActivitiesCountString(otherActivities.length)}
                                    />
                                </ListItem>
                            </Fragment>
                        );
                    })()}
                </List>
            </ContentLoader>
        </DetailPage>
    );
});

export default ValuesInventoryHome;
