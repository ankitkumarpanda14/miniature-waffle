import requests
import ast

def convert_command_to_plan(user_command: str) -> list:
    """
    Sends user input to the Ollama model and returns a list of actions for the robot to execute.
    """
    system_prompt = (
        "You are a robot control planner. "
        "The robot operates in a 10x10 grid and understands only these commands: "
        "move_forward, turn_left, turn_right, dock. "
        "Given an instruction, respond with a Python list like: "
        '["move_forward", "turn_left", "dock"]. No explanation. Output only valid Python.'
    )

    full_prompt = f"{system_prompt}\n\nInstruction: {user_command}\n\nOutput:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:1b",
                "prompt": full_prompt,
                "stream": False
            },
            timeout=10
        )
        output = response.json()["response"].strip()

        # Use safe evaluation
        actions = ast.literal_eval(output)
        if isinstance(actions, list) and all(isinstance(a, str) for a in actions):
            return actions
        else:
            print("⚠️ Unexpected output:", output)
    except Exception as e:
        print("❌ LLM error:", e)

    return []
