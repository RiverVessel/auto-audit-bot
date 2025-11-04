import os
import subprocess
import json
import openai

TARGET = os.getenv("TARGET_REPO")
if not TARGET:
    raise ValueError("TARGET_REPO environment variable not set")

# Clone target repository
os.system("rm -rf target_repo && git clone {} target_repo".format(TARGET))

# Run Slither analysis
os.chdir("target_repo")
subprocess.run(["slither", ".", "--json", "../report.json"], check=False)
os.chdir("..")

# Load analysis report
with open("report.json") as f:
    report = json.load(f)

# Summarize issues using OpenAI GPT model
openai.api_key = os.getenv("OPENAI_API_KEY")
issues = report.get("results", [])
prompt = "Summarize these Solidity issues for an Immunefi bug bounty report:\n" + str(issues)
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": prompt}]
)
summary = response["choices"][0]["message"]["content"]

# Write summary to file
with open("summary.md", "w") as f:
    f.write(summary)
