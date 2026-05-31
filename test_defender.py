import asyncio, json
from defender import Defender

async def main():
    finding = {
        "type": "eval",
        "file_path": "sample_vulnerable_code/vuln.py",
        "line": 6,
        "line_text": "return eval(user_input)"
    }
    defender = Defender()
    patch = await defender.generate_patch(finding)
    print(json.dumps(patch, indent=2))

asyncio.run(main())
