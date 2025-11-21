import signal
import sys
import argparse
import os
import datetime
import json

from aiss_ollama_chat_autonomous.chat import OllamaChatAutonomous

AUTO:bool = False

def main():
    def signalHandler(sig, frame):
        global AUTO
        if AUTO:
            print("\nAUTO OFF\n")
            AUTO = False
        return

    signal.signal(signal.SIGINT, signalHandler)
    parser = argparse.ArgumentParser(
        description='Ollama autonomous assistant-assistant chat app.',
        epilog='Example: ollama-chat-autonomous gemma3:12b-it-q8_0 gemma3:12b-it-q8_0 sysPromptA.txt sysPromptB.txt -u MyName -l 20 -t 20 -a False'
    )
    
    parser.add_argument('modelA', help='Model (A) to use')
    parser.add_argument('modelB', help='Model (B) to use')
    parser.add_argument('sysPromptA', help='Plain text file with the system prompt (A)')
    parser.add_argument('sysPromptB', help='Plain text file with the system prompt (B)')
    parser.add_argument('--userName', '-u', type=str, default="User",
                    help='User name (default: "User")')
    parser.add_argument('--maxLength', '-l', type=int, default=20,
                    help='Maximum context lenght (default: 20)')
    parser.add_argument('--startAuto', '-a', type=bool, default=False,
                    help='Indicate if loop starts on auto chat (default: True)')

    args = parser.parse_args()

    chat = OllamaChatAutonomous(args.modelA, args.modelB, args.sysPromptA, args.sysPromptB, args.userName, args.maxLength)
    global AUTO
    AUTO = args.startAuto
    prompt = " "

    while True:
        try:
            if AUTO:
                msg1, msg2 = chat.doRecursiveChat()
                print(f"{msg1}{msg2}")
            else:
                prompt = input(f"{chat.userName}: ")
                if prompt.startswith("auto"):
                    AUTO = True
                elif prompt.startswith("exit"):
                    print("Good bye!")
                    break
                else:
                    print(f"{chat.chat(prompt)}\n\n")
        except EOFError:
            print("\n--FORCE EXIT--")
            sys.exit(0)
        except Exception as e:
            print(f"{e}\n\n")
    chat.makeBackup()


if __name__ == "__main__":

    main()
