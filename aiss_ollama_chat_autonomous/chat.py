from aiss_ollama_chat.chat import Chat
from aiss_ollama_chat.fileIO import FileIO

class OllamaChatAutonomous:
    def __init__(self, model1:str, model2:str, sysPrompt1:str, sysPrompt2:str, userName:str="User", maxChatLength:int=20):
        self.userName = userName
        self.c1:Chat = Chat(model1, sysPrompt1, maxChatLength, userName)
        self.c2:Chat = Chat(model2, sysPrompt2, maxChatLength, userName)
        self.lastMsg = " "
        self.operations = {
            "save": self._handleSave,
            "restore": self._handleRestore,
            "rewind": self._handleRewind,
            "A:": self._handleChatA,
            "B:": self._handleChatB,
            "AB:": self._handleChatAB
        }

    def autoChat(self, turns):
        if turns < 0: raise Exception(f"Invalid num. turns. Param: {turns}")
        while turns != 0:
            self.doRecursiveChat()
            turns -= 1
    
    def doRecursiveChat(self, prompt:str=None):
        if prompt:
            self.c1.chatHistory.append(self.c1.strMsg("user",prompt))
        msg = self.c1.chat(self.lastMsg)
        if prompt:
            self.c2.chatHistory.append(self.c2.strMsg("user",prompt))
        self.lastMsg = self.c2.chat(msg)
        return msg, self.lastMsg

    def doChatA(self, prompt):
        return self.c1.chat(prompt)
    
    def doChatB(self, prompt):
        return self.c2.chat(prompt)
    
    def chat(self, prompt):
        try:
            for operation, handler in self.operations.items():
                if prompt.startswith(operation):
                    return handler(prompt)
            return self._handleDefault(prompt)
        except Exception as e:
            raise Exception(e)

    def _handleSave(self, prompt: str) -> str:
        if prompt.startswith("save:"):
            # path = prompt[len("save:"):].strip()
            # return f"-- serialized to {path} --\n\n"
            raise Exception("Unimplemented")
        else:
            self.c1.chat("save:context1.json")
            self.c2.chat("save:context2.json")
            return "-- serialized to ./context1.json and ./context2.json --\n\n"

    def _handleRestore(self, prompt: str) -> str:
        if prompt.startswith("restore:"):
            # path = prompt[len("restore:"):].strip()
            # return f"-- restored from {path} --\n\n"
            raise Exception("Unimplemented")
        else:
            self.c1.chat("restore:context1.json")
            self.c2.chat("restore:context2.json")
            self.chatHistory = FileIO.deserializeDict("./context.json")
            return "-- restored from ./context1.json and ./context2.json --\n\n"

    def _handleRewind(self, prompt: str) -> str:
        if prompt.startswith("rewind:"):
            amount = int(prompt[len("rewind:"):].strip())
            self.c1.rewind(amount)
            self.c2.rewind(amount)
            return f"-- rewind AB: {amount} --\n\n"
        else:
            self.c1.rewind(1)
            self.c2.rewind(1)
            return "-- rewind AB: 1 --\n\n"
        
    def _handleChatA(self, prompt):
        return f"{self.doChatA(prompt[len('A:'):].strip())}"

    def _handleChatB(self, prompt):
        return f"{self.doChatB(prompt[len('B:'):].strip())}"

    def _handleChatAB(self, prompt):
        msg1 = f"{self.doChatA(prompt[len('A:'):].strip())}"
        msg2 = f"{self.doChatB(prompt[len('B:'):].strip())}"
        return f"{msg1}{msg2}"
    
    def _handleDefault(self, prompt):
        self.lastMsg = self.c2.getLastContextMsg()
        msg1, msg2 = self.doRecursiveChat(prompt)
        return f"{msg1}{msg2}"

    def makeBackup(self) -> None:
        self.c1.makeBackup("Chat-A")
        self.c2.makeBackup("Chat-B")
