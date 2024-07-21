import { useEffect, useState } from "react";
import {
  ChakraProvider,
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Input,
  Button,
  Checkbox,
  FormControl,
  FormLabel,
  useToast,
  Flex,
} from "@chakra-ui/react";
import axios from "axios";

type Player = {
  "Starting Balance": number;
  "Final Balance": number;
  "Net Balance": number;
  "Single Wins": number;
  "Double Wins": number;
  "Total Wins": number;
  Active: boolean;
};

function App() {
  const [players, setPlayers] = useState<Record<string, Player>>({});
  const [newPlayerName, setNewPlayerName] = useState("");
  const [newPlayerBalance, setNewPlayerBalance] = useState("");
  const [selectedWinner, setSelectedWinner] = useState("");
  const [isDouble, setIsDouble] = useState(false);
  const toast = useToast();

  const loadPlayers = async () => {
    try {
      const response = await axios.get("http://192.168.18.97:5000/get_players");
      setPlayers(response.data);
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

  useEffect(() => {
    loadPlayers();
  }, []);

  const handleAddPlayer = async () => {
    try {
      await axios.post("http://192.168.18.97:5000/add_player", {
        name: newPlayerName,
        balance: parseFloat(newPlayerBalance),
      });
      toast({
        title: "Player added.",
        status: "success",
        duration: 2000,
        isClosable: true,
      });
      setNewPlayerName("");
      setNewPlayerBalance("");
      loadPlayers();
    } catch (error) {
      console.error("Error adding player:", error);
      toast({
        title: "Error adding player.",
        status: "error",
        duration: 2000,
        isClosable: true,
      });
    }
  };

  const handleUpdateWinner = async () => {
    try {
      await axios.post("http://192.168.18.97:5000/update_winner", {
        winner: selectedWinner,
        double: isDouble ? 2 : 1,
      });
      toast({
        title: "Winner updated.",
        status: "success",
        duration: 2000,
        isClosable: true,
      });
      setSelectedWinner("");
      setIsDouble(false);
      loadPlayers();
    } catch (error) {
      console.error("Error updating winner:", error);
      toast({
        title: "Error updating winner.",
        status: "error",
        duration: 2000,
        isClosable: true,
      });
    }
  };

  const handleClearData = async () => {
    try {
      await axios.post("http://192.168.18.97:5000/clear_data");
      toast({
        title: "Data cleared and saved to Excel.",
        status: "success",
        duration: 2000,
        isClosable: true,
      });
      loadPlayers();
    } catch (error) {
      console.error("Error clearing data:", error);
      toast({
        title: "Error clearing data.",
        status: "error",
        duration: 2000,
        isClosable: true,
      });
    }
  };

  const handleDeactivatePlayer = async (name: string) => {
    try {
      await axios.post("http://192.168.18.97:5000/deactivate_player", {
        name: name,
      });
      toast({
        title: `Player ${name} has been deactivated.`,
        status: "success",
        duration: 2000,
        isClosable: true,
      });
      loadPlayers();
    } catch (error) {
      console.error(`Error deactivating player ${name}:`, error);
      toast({
        title: `Error deactivating player ${name}.`,
        status: "error",
        duration: 2000,
        isClosable: true,
      });
    }
  };

  const handleActivatePlayer = async (name: string) => {
    try {
      await axios.post("http://192.168.18.97:5000/activate_player", {
        name: name,
      });
      toast({
        title: `Player ${name} has been activated.`,
        status: "success",
        duration: 2000,
        isClosable: true,
      });
      loadPlayers();
    } catch (error) {
      console.error(`Error activating player ${name}:`, error);
      toast({
        title: `Error activating player ${name}.`,
        status: "error",
        duration: 2000,
        isClosable: true,
      });
    }
  };

  const handleUndoLastWin = async () => {
    try {
      await axios.post("http://192.168.18.97:5000/undo_last_win");
      toast({
        title: "Last win has been undone.",
        status: "success",
        duration: 2000,
        isClosable: true,
      });
      loadPlayers();
    } catch (error) {
      console.error("Error undoing last win:", error);
      toast({
        title: "Error undoing last win.",
        status: "error",
        duration: 2000,
        isClosable: true,
      });
    }
  };

  return (
    <ChakraProvider>
      <Box p={4} overflowX="scroll">
        <Heading mb={4} fontSize={{ base: 23, md: 30 }}>
          Player Management
        </Heading>

        <Heading size="md" mt={8} mb={4}>
          Players
        </Heading>
        <Table
          size="md"
          variant="striped"
          colorScheme="purple"

          // overflowWrap={"break-word"}
        >
          <Thead bgColor="blue.100">
            <Tr>
              <Th color="black">Name</Th>
              <Th color="black">Starting Balance</Th>
              <Th color="black">Final Balance</Th>
              <Th color="black">Net Balance</Th>
              <Th color="black">Single Wins</Th>
              <Th color="black">Double Wins</Th>
              <Th color="black">Total Wins</Th>
              <Th color="black">Active</Th>
              <Th color="black">Actions</Th>
            </Tr>
          </Thead>
          <Tbody>
            {Object.entries(players).map(([name, player]) => (
              <Tr key={name}>
                <Td>{name}</Td>
                <Td>{player["Starting Balance"]}</Td>
                <Td>{player["Final Balance"]}</Td>
                <Td>{player["Net Balance"]}</Td>
                <Td>{player["Single Wins"]}</Td>
                <Td>{player["Double Wins"]}</Td>
                <Td>{player["Total Wins"]}</Td>
                <Td>{player.Active ? "Yes" : "No"}</Td>
                <Td>
                  <Flex>
                    <Button
                      size="sm"
                      colorScheme="red"
                      onClick={() => handleDeactivatePlayer(name)}
                      mr={2}
                      disabled={!player.Active}
                    >
                      Leave
                    </Button>
                    <Button
                      size="sm"
                      colorScheme="green"
                      onClick={() => handleActivatePlayer(name)}
                      mr={2}
                      disabled={player.Active}
                    >
                      Join
                    </Button>
                  </Flex>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>

        <Heading size="md" mt={8} mb={4}>
          Add Player
        </Heading>
        <FormControl mb={4}>
          <FormLabel>New Player Name</FormLabel>
          <Input
            value={newPlayerName}
            onChange={(e) => setNewPlayerName(e.target.value)}
          />
        </FormControl>
        <FormControl mb={4}>
          <FormLabel>New Player Balance</FormLabel>
          <Input
            value={newPlayerBalance}
            onChange={(e) => setNewPlayerBalance(e.target.value)}
          />
        </FormControl>
        <Button onClick={handleAddPlayer}>Add Player</Button>

        <Heading size="md" mt={8} mb={4}>
          Update Winner
        </Heading>
        <FormControl mb={4}>
          <FormLabel>Select Winner</FormLabel>
          <Input
            value={selectedWinner}
            onChange={(e) => setSelectedWinner(e.target.value)}
          />
        </FormControl>
        <Checkbox
          isChecked={isDouble}
          onChange={(e) => setIsDouble(e.target.checked)}
          size="lg"
          mt="7px"
        >
          Double Win
        </Checkbox>
        <br />
        <Button onClick={handleUpdateWinner} colorScheme="purple" mt="20px">
          Update Winner
        </Button>

        <Heading size="md" mt={8} mb={4}>
          Actions
        </Heading>
        <Button onClick={handleClearData} colorScheme="red" mr={4} mb={4}>
          Clear Data and Save to Excel
        </Button>
        <Button onClick={handleUndoLastWin} colorScheme="yellow" mb={4}>
          Undo Last Win
        </Button>
      </Box>
    </ChakraProvider>
  );
}

export default App;
