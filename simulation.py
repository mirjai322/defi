'''
This is the main program that kicks off the simulation process. It defines all the config properties that are used by the simulation.
It runs  6 scenarios
1. Centralized System with Low Gov Regulations
2. Centralized System with Medium Gov Regulations
3. Centralized System with High Gov Regulations
4. De-Centralized System with Low Gov Regulations
5. De-Centralized System with Medium Gov Regulations
6. De-Centralized System with High Gov Regulations

For each scenario an output folder is created.
The details of each "run" are in a "detail_data_iterationXXX.csv file
There is a summary file created that provides statistical information like max, min, stddev for
all the agents, firms and regulators

'''

from agents import Agent
from firms import Firm
from regulators import Regulator
from numpy import random
from environment import Economy
import shutil
import os
import csv
'''
config is used to configure simulation. You can control how many agents, firms , regulators to create
'''
config = {
  "agents": {
    "num_agents": 100,
    "agent_action_space": ['invest'],
    "agent_state_space": ['money'],  # Name of variable
    "reward_function": ["money_agents"],
    "roi_rate_high":0.1,
    "roi_rate_middle": 0.03,
    "roi_rate_low": 0.01,

  },
  "firms": {
    "num_firms": 10,
    "firm_action_space": ['fee_rate'],
    "firm_state_space": ['money'],
    "reward_functions": ["money_firms"],
    "min_transaction_fee_low":0.001,
    "max_transaction_fee_low":0.05,
    "min_transaction_fee_medium": 0.005,
    "max_transaction_fee_medium": 0.009,
    "min_transaction_fee_high": 0.001,
    "max_transaction_fee_high": 0.003,

  },
  "regulators": {
    "num_regulators": 1,  # Leave as 1, there is just 1 gov.
    "reg_action_space": ['fee_rate', 'tax_rate'],
    "tax_rate_agents": 0.10,
    "tax_rate_firms": 0.10,
    "min_tax_rate_agents_low": 0,
    "max_tax_rate_agents_low": 0,
    "min_tax_rate_agents_medium": 0.005,
    "max_tax_rate_agents_medium": 0.01,
    "min_tax_rate_agents_high": 0.01,
    "max_tax_rate_agents_high": 0.07,
    "min_tax_rate_firms_low": 0,
    "max_tax_rate_firms_low": 0,
    "min_tax_rate_firms_medium": 0.005,
    "max_tax_rate_firms_medium": 0.01,
    "min_tax_rate_firms_high": 0.03,
    "max_tax_rate_firms_high": 0.05,

    "merger_threshold_low": 1.0,
    "merger_threshold_medium": 0.60,
    "merger_threshold_high": 0.30,

    "min_interest_rate_low": 0.03,
    "max_interest_rate_low": 0.16,
    "min_interest_rate_medium": 0.07,
    "max_interest_rate_medium": 0.10,
    "min_interest_rate_high": 0.03,
    "max_interest_rate_high": 0.05,

    "min_gov_aid_agent_low": 0,
    "max_gov_aid_agent_low": 0,
    "min_gov_aid_agent_medium": 0.010,
    "max_gov_aid_agent_medium": 0.02,
    "min_gov_aid_agent_high": 0.12,
    "max_gov_aid_agent_high": 0.17,

    "min_gov_aid_firm_low": 0,
    "max_gov_aid_firm_low": 0,
    "min_gov_aid_firm_medium": 0.001,
    "max_gov_aid_firm_medium": 0.02,
    "min_gov_aid_firm_high": 0.02,
    "max_gov_aid_firm_high": 0.05,


    "reg_state_space": ['wealth_equality', 'money'],
    "reward_functions": ['money_firms_agents', 'equality_agents']
    # Equality could be measured by the standard deviation of agents (smaller is better). Could make this a negative number
  },
  "general": {
    "save_state_iterations": 10,
    "simulation_run_count": 50,
    "iterations_in_each_simulation_run": 800,
    "mode":"centralized",
    "regulation_mode":"low",
  }
}

'''
simulate centralized world interactions 
'''
def do_centralized_world_interactions(environment, i):
  # Agents interact with each other
  environment.interact_agents_with_agents()

  # Agents interact with firms
  environment.interact_firms_with_agents()

  # Firms interact with firms
  if i%53 == 0:
    environment.interact_firms_with_firms()

  # Government regulate firms (maybe penalize)
  if i % 52 == 0:
    environment.regulators_regulate_firms()

  # Government regulate individuals
  if i % 52 == 0:
    environment.regulators_regulate_agents()

  # give some ROI for the networth that is sitting in agent's account assume they invested it in different places
  if i %24 == 0:
    environment.agent_earn_roi()

  # Government giving aid
  if i%25 == 0:
    environment.gov_giving_aid()

'''
simulate de-centralized world interactions 
'''
def do_decentralized_world_interactions(environment, i):
  # Agents decide interest rate and give a cut to Crypto firms 
  environment.decentralized_lending()

  # Government regulate firms
  if i % 52 == 0:
    environment.regulators_regulate_firms()

  # Government regulate individuals
  if i % 52 == 0:
    environment.regulators_regulate_agents()

  # Agent-agent interaction (betting)
  environment.interact_agents_with_agents()

  # decentralized encourages lending and betting between poor/middle class
  environment.interact_underrep_agents_with_agents()
  environment.decentralized_lending_for_underrep()

  # Government giving aid
  if i%53 == 0:
    environment.gov_giving_aid()

  # give some ROI for the networth that is sitting in agent's account assume they invested it in different places
  if i %24 == 0:
    environment.agent_earn_roi()

def simulate(config, simulation_run_number, is_centralized):
  environment = Economy(config, is_centralized)
  environment.configure_agents()
  environment.configure_firms()
  environment.configure_regulators()

  num_iterations = config["general"]["iterations_in_each_simulation_run"]
  for i in range(1, num_iterations + 1):
    if is_centralized:
      do_centralized_world_interactions(environment, i)
    else:
      do_decentralized_world_interactions(environment, i)

    # Modulo operator = "remainder operator"
    if (i == 1 or i == num_iterations
        or (i) % config['general']['save_state_iterations'] == 0):
      environment.save_state(i)
    # all iterations done -- now print the state to a csv file for further analysis
  environment.print_state(simulation_run_number)
  return environment.summary

def cleanOutputFolder(mode,regulation):
  folder_path = mode+"_"+regulation+"_output"
  try:
    shutil.rmtree(folder_path)
  except:
    print("could not delete the folder")
  os.mkdir(folder_path)



def run(mode, regulation):
  # set the mode and regulation in the config object so that it can be used by other classes
  config["general"]["mode"] = mode
  config["general"]["regulation_mode"] = regulation

  #clean up the specific output folder for the mode+regulation
  cleanOutputFolder(mode, regulation)
  if mode == "centralized":
    is_centralized = True
  else:
    is_centralized = False

  summary_of_all_runs = []
  # run simulate N times with M Iterations (time steps) in each run
  for i in range(config["general"]["simulation_run_count"]):
    summary_data_for_onerun = simulate(config, i, is_centralized)
    summary_of_all_runs.extend(summary_data_for_onerun)

  # write summary of all the  runs into a csv file
  filename = mode + "_"+ regulation+ "_output/summary.csv"
  list = summary_of_all_runs
  #write the header of the csv file
  with open(filename, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list[0].keys())
    writer.writeheader()

  #write the content of the array to csv file
  with open(filename, 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list[0].keys())
    for row in list:
      writer.writerow(row)


#start the simulation
run("decentralized", "low")
run("decentralized", "medium")
run("decentralized", "high")
run("centralized", "low")
run("centralized", "medium")
run("centralized", "high")

print("Simulation completed successfully!! Please check the output folders")