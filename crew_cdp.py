import os
from cdp import *
from crewai import Agent, Task, Crew, Process

# Set up environment variables for model and API key

# Configure CDP SDK
Cdp.configure_from_json("cdp_api_key.json")  # Ensure this file contains the API keys
print("CDP SDK has been successfully configured with CDP API key.")

# Create a Payment Agent
payment_agent = Agent(
    role="Payment Agent",
    goal="Distribute bounties to wallet addresses securely and efficiently.",
    verbose=True,
    memory=False,
    backstory=(
        "You are a blockchain payment processor ensuring secure, fast, and accurate bounty "
        "distributions using CDP Wallet APIs."
    )
)

# Task to execute payment
payment_task = Task(
    description=(
        "Take the wallet address `{wallet_address}` and distribute `{amount}` bounty in `{currency}`. "
        "Ensure the transaction completes successfully and verify the transfer."
    ),
    expected_output="A confirmation of the successful bounty transfer, including transaction details.",
    tools=[],
    agent=payment_agent
)

# Crew and Process
crew = Crew(
    agents=[payment_agent],
    tasks=[payment_task],
    process=Process.sequential  # Ensures the task is executed sequentially
)

# Function to Distribute Bounty
def distribute_bounty(wallet_address, amount, currency="eth"):
    # Create a wallet with one address by default.
    wallet1 = Wallet.create()
    print(f"Wallet successfully created: {wallet1}")

    # Fund the wallet with a faucet transaction.
    faucet_tx = wallet1.faucet()
    faucet_tx.wait()
    print(f"Faucet transaction successfully completed: {faucet_tx}")
    if not len(wallet_address):
        wallet_address = Wallet.create()


    # Perform transfer to target wallet address.
    transfer = wallet1.transfer(amount, currency, wallet_address).wait()
    print(f"Transfer successfully completed: {transfer}")

    return transfer



# Example Input
inputs = {"wallet_address": "", "amount": 0.0001, "currency": "eth"}

# Crew Execution
result = crew.kickoff(inputs=inputs)

# Perform Bounty Distribution
distribute_bounty(inputs["wallet_address"], inputs["amount"], inputs["currency"])
