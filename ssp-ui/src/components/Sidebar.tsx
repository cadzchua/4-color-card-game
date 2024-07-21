import { AtSignIcon, CalendarIcon } from "@chakra-ui/icons";
import { Badge, List, ListIcon, ListItem } from "@chakra-ui/react";
import { NavLink } from "react-router-dom";

const Sidebar = () => {
  return (
    <List color="white" fontSize="1.2em" spacing={4} p="0px" mb="0px">
      <ListItem>
        <NavLink to="/">
          <ListIcon as={CalendarIcon} color="white" m="2px 7px 2px 7px" />
          Home
        </NavLink>
      </ListItem>
      <ListItem>
        <NavLink to="/">
          {/* change to to="/profile" when ready */}
          <Badge colorScheme="yellow" mb={1}>
            Coming Soon
          </Badge>
          <ListIcon as={AtSignIcon} color="white" m="2px 7px 2px 7px" />
          Profile
        </NavLink>
      </ListItem>
    </List>
  );
};

export default Sidebar;
