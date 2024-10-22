# NFTicket - Smart Contract for Event Management with NFT Integration

## Overview
NFTicket is a smart contract built on the Algorand blockchain, which integrates NFT (Non-Fungible Token) management for events. It enables users to create, store, and manage events associated with unique NFT IDs and specific end timestamps. The smart contract also supports event stopping, ticket issuance, and managing attendants.

## Features

### 1. **Contract Creation**
   - **Functionality:** Upon deployment, the contract initializes the `event_count` to `0`, which tracks the total number of events created.
   - **Log Output:** 
     - `"Creating contract, initializing event_count to 0"`

### 2. **Create Event**
   - **Functionality:** Allows the creator to create a new event by specifying the NFT ID, end timestamp, and total number of tickets.
   - **Steps:**
     - Checks that the current number of events is within the allowed maximum (`MAX_EVENTS`).
     - Increments the `event_count`.
     - Stores the NFT ID, end timestamp, and ticket details in the global state.
   - **Log Output:**
     - `"Handling create_event"`
     - `"Incremented event_count"`
     - `"Stored nft_id and end_timestamp"`
     - `"Ticket information stored"`

### 3. **Stop Event**
   - **Functionality:** Stops an event when its end timestamp has passed by updating the state.
   - **Steps:**
     - Ensures the event ID is valid.
     - Verifies the current timestamp is greater than the event's end time.
     - Marks the event as stopped.
   - **Log Output:**
     - `"Handling stop_event"`
     - `"Event has been stopped"`

### 4. **Register Attendant**
   - **Functionality:** Registers attendants for an event by updating their status and issuing tickets.
   - **Steps:**
     - Verifies the event has available tickets.
     - Registers the attendant in local state and updates ticket counts.
   - **Log Output:**
     - `"Attendant registered"`
     - `"Tickets updated"`

### 5. **Transaction Logging**
   - **Functionality:** Logs are created at key transaction points, including event creation, ticket issuance, and event stopping.
   - **Purpose:** Assists with debugging and ensures transparency.

### 6. **Application JSON Spec (ARC-4 Compliant)**
   - **Functionality:** The smart contract generates an ARC-4 compliant `application.json`, containing supported methods, global state schema, and descriptions of the available functions.
   - **Purpose:** Ensures compatibility with Algorand tools and simplifies integration.

## How to Use

1. **Contract Creation:**
   - Deploy the contract using the Algorand SDK. The contract will initialize `event_count` to `0`.

2. **Create Event:**
   - Call the `create_event` method with:
     - `nft_id`: The NFT ID for the event.
     - `end_timestamp`: Timestamp when the event ends.
     - `ticket_count`: The total number of tickets for the event.

3. **Stop Event:**
   - After an event's end time, call the `stop_event` method with the `event_id` to stop the event.

4. **Register Attendant:**
   - Call the `add_attendant` method to register an attendant and issue a ticket.

## Global State Variables

- **event_count**: Tracks the total number of events created.
- **event_x_nft_id**: Stores the NFT ID for each event.
- **event_end_x**: Stores the end timestamp for each event.
- **event_stopped_x**: Indicates whether an event has been stopped.
- **event_ticket_count_x**: Tracks remaining tickets for an event.
- **event_ticket_issued_x**: Tracks issued tickets for an event.

## Methods

- **create_event(uint64 nft_id, uint64 end_timestamp, uint64 ticket_count)**: Creates a new event with the specified NFT ID, end time, and ticket count. Returns `1` on success.
- **stop_event(uint64 event_id)**: Stops an event. Returns `1` on success.
- **add_attendant(uint64 event_id)**: Registers an attendant and issues a ticket for the specified event.

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/FlamoDynamo/NFTicket.git
   cd NFTicket

2. **Install Dependencies:**
Make sure you have Algorand SDK installed and set up your environment variables (Algorand node address and API key).

3. **Compile Smart Contract:**
Use PyTeal to compile the smart contract files:
  ```bash
  python smart_contracts/contract/contract.py
  ```

4. **Deploy the Smart Contract:**
After compiling, deploy the contract using Algorand SDK or Algokit and store the `application ID`.

**In addition to the above functions, the project also has a check-in function at the gate using the wallet information containing the requested NFT of the attending guests.**

**---**

Welcome to your new AlgoKit project!

This is your workspace root. A `workspace` in AlgoKit is an orchestrated collection of standalone projects (backends, smart contracts, frontend apps and etc).

By default, `projects_root_path` parameter is set to `projects`. Which instructs AlgoKit CLI to create a new directory under `projects` directory when new project is instantiated via `algokit init` at the root of the workspace.

## Getting Started

To get started refer to `README.md` files in respective sub-projects in the `projects` directory.

To learn more about algokit, visit [documentation](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md).

### GitHub Codespaces

To get started execute:

1. `algokit generate devcontainer` - invoking this command from the root of this repository will create a `devcontainer.json` file with all the configuration needed to run this project in a GitHub codespace. [Run the repository inside a codespace](https://docs.github.com/en/codespaces/getting-started/quickstart) to get started.
2. `algokit init` - invoke this command inside a github codespace to launch an interactive wizard to guide you through the process of creating a new AlgoKit project

Powered by [Copier templates](https://copier.readthedocs.io/en/stable/).
