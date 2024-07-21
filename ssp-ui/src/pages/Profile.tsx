import { AtSignIcon, InfoIcon, StarIcon } from "@chakra-ui/icons";
import {
  List,
  ListIcon,
  ListItem,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";

const Profile = () => {
  return (
    <Tabs
      mt="20px"
      p="20px"
      pb="0px"
      pt="0px"
      colorScheme="purple"
      variant="enclosed"
    >
      <TabList>
        <Tab _selected={{ color: "white", bg: "purple.400" }}>Account Info</Tab>
        <Tab _selected={{ color: "white", bg: "purple.400" }}>Win History</Tab>
      </TabList>

      <TabPanels>
        <TabPanel p="10px">
          <List spacing={3} p="0px" mb="0px">
            <ListItem>
              <ListIcon as={AtSignIcon} />
              cadden
            </ListItem>
            <ListItem>
              <ListIcon as={StarIcon} />
              Never Give up!
            </ListItem>
          </List>
        </TabPanel>
        <TabPanel>
          <List spacing={3} p="0px" mb="0px">
            <ListItem>
              <ListIcon as={InfoIcon} />
              Number of Single Wins: 1
            </ListItem>
            <ListItem>
              <ListIcon as={InfoIcon} />
              Number of Single Wins: 1
            </ListItem>
            <ListItem>
              <ListIcon as={InfoIcon} />
              Number of Total Wins: 2
            </ListItem>
          </List>
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
};

export default Profile;
