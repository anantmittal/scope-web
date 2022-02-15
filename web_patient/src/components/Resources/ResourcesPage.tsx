import { Divider, List, ListItem } from '@mui/material';
import React, { FunctionComponent } from 'react';
import { Link } from 'react-router-dom';
import ListCard from 'src/components/common/ListCard';
import { MainPage } from 'src/components/common/MainPage';
import Section from 'src/components/common/Section';
import { getImage } from 'src/services/images';
import { getFormPath, ParameterValues, Routes } from 'src/services/routes';
import { getString } from 'src/services/strings';

export const ResourcesPage: FunctionComponent = () => {
    return (
        <MainPage title={getString('Navigation_resources')}>
            <Section>
                <List>
                    <ListItem
                        alignItems="flex-start"
                        disableGutters={true}
                        component={Link}
                        to={Routes.valuesInventory}>
                        <ListCard
                            title={getString('Resources_inventory_title')}
                            subtitle={getString('Resources_inventory_subtitle')}
                            imageSrc={getImage('Resources_values_button_image')}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem alignItems="flex-start" disableGutters={true} component={Link} to={Routes.worksheets}>
                        <ListCard
                            title={getString('Resources_resources_title')}
                            subtitle={getString('Resources_resources_subtitle')}
                            imageSrc={getImage('Resources_worksheets_button_image')}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem
                        alignItems="flex-start"
                        disableGutters={true}
                        component={Link}
                        to={getFormPath(ParameterValues.form.safetyPlan)}>
                        <ListCard
                            title={getString('Resources_safety_plan_title')}
                            subtitle={getString('Resources_safety_plan_subtitle')}
                            imageSrc={getImage('Resources_safety_button_image')}
                        />
                    </ListItem>
                </List>
            </Section>
        </MainPage>
    );
};

export default ResourcesPage;
