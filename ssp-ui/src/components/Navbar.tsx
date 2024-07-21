import {
  Flex,
  Heading,
  Spacer,
  HStack,
  Text,
  Button,
  Avatar,
  Badge,
} from "@chakra-ui/react";

function Navbar() {
  return (
    <Flex bg="red.200" as="nav" p="10px" alignItems="center">
      <Heading as="h1" mt={1} fontSize={{ base: "3xl", lg: "4xl" }}>
        四色牌
      </Heading>
      <Spacer />
      <HStack spacing="20px">
        <Avatar bg="purple.400" size="md" src="src/assets/ssp.jpg"></Avatar>
        <Text m="0px">User</Text>
        <Button isDisabled={true} colorScheme="blue">
          {/* New feature removed when it is working */}
          {/* <Badge colorScheme="yellow">Coming Soon</Badge> */}
          <Text
            mb="1px"
            textTransform="uppercase"
            fontWeight="bold"
            color="white"
          >
            Logout
          </Text>
        </Button>
      </HStack>
    </Flex>
  );
}

export default Navbar;
