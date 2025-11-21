# Ollama Chat - Chatbot with Ollama

This project implements an autonomous chat system using Ollama, where two artificial intelligence models interact with each other in a continuous conversation.

## 📋 Description

The project allows creating an autonomous chat where two language models communicate with each other, generating a continuous conversation. Each model acts as a different participant in the conversation, responding to messages from the other model.

## 🚀 Features

The app allows two chatbots to communicate each other: 
- Model A receives an initial message and responds
- Model B receives the first model's response and responds
- This process repeats for the specified number of turns
- Logs are saved to a json file
- Autonomous and manual mode. Switch to manual with Cntrl+C (on auto).
- Text commands to chat
  - `auto` - Starts autonomous mode.
  - `A:` - Sends the next prompt only to model A.
  - `B:` - Sends the next prompt only to model B.
  - `AB:` - Sends the next prompt only to model A and B (no msg pass between models).
- Allows recursive commands (e.g.: `A:save`, `B:rewind:2`)
  - `exit` - Exits app with a backup save at run path.
  - `save` - Stores a conversational context file named "context.json" at run path.
  - `save:` - Stores a conversational context file at path inidicated next, related to run path.
  - `restore` - Restores a conversational context file at "context.json" located at run path.
  - `restore:` - Restores a conversational context file at path inidicated next, related to run path.
  - `rewind` - Goes back to a previous turn.
  - `rewind:` - Goes back an ammount of turns indicated next.
- Flow control keyboard commands:
  - `Cntrl+C` - Stops AUTO mode.
  - `Cntrl+D` - Forces App exit (during input)
     
## 🛠 Requirements

- Python 3.7+
- Ollama installed and running
- Required packages:
  - `ollama`
  - `aiss_ollama_chat`

## 📦 Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Clone the repository:
   ```bash
   git clone <your-repository>
   cd ollamaChat
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install package using:
   ```bash
   pip install .
   ```

## ▶️ Usage

Run the program with:
```bash
ollama-chat-autonomous <model1> <model2> <prompt1> <prompt2> <numTurns> <maxLength>
```

Example:
```bash
ollama-chat-autonomous gemma3:12b-it-q8_0 gemma3:12b-it-q8_0 ./sysPrompt1.txt ./sysPrompt2.txt 10 10
```

## 📁 Project Structure

```
.
├── aiss_ollama_chat_autonomous/
│   ├── __init__.py
│   ├── chat.py
│   └── run.py
├── run.sh
├── setup.py
├── LICENSE
└── README.md
```

## 📄 Output

Conversation history is saved in a timestamped folder:
```
Chat-A_2025-11-09_21-00-00/
├── log.sh
└── params.py
Chat-B_2025-11-09_21-00-00/
├── log.sh
└── params.py
```

## 🤝 Contributions

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.