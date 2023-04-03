import math

from agents import Agent
from firms import Firm
from regulators import Regulator
from numpy import random
import numpy as np
from ledger import Ledger
import csv


class Economy:

  def __init__(self, config, is_centralized):
    self.config = config
    self.num_agents = config["agents"]["num_agents"]
    self.num_firms = config["firms"]["num_firms"]
    self.num_regulators = config["regulators"]["num_regulators"]
    self.state = []
    self.summary = []
    self.ledger = Ledger()
    self.is_centralized = is_centralized
    print("configuration based on regulation setup::::")
    print(self.get_min_tax_rate_agents())
    print(self.get_max_tax_rate_agents())
    print(self.get_min_tax_rate_firms())
    print(self.get_max_tax_rate_firms())
    print(self.get_min_interest_rate())
    print(self.get_max_interest_rate())
    print(self.get_min_tranaction_fee())
    print(self.get_max_tranaction_fee())

  def configure_agents(self):
    self.agents = []
    total_agents = self.config['agents']['num_agents']
    total_rich_agents = math.ceil(total_agents*0.05)
    total_poor_agents = math.ceil(total_agents*0.20)
    total_middle_agents = total_agents - total_rich_agents - total_poor_agents

    for i in range(total_rich_agents):
      a = Agent(self.config['agents'])
      rand_num = random.randint(1, 2)
      a.net_worth = rand_num * 10000000
      a.subtype = "High"
      self.agents.append(a)

    for i in range(total_middle_agents):
      a = Agent(self.config['agents'])
      a.subtype = "Middle"
      rand_num = random.randint(1, 2)
      a.net_worth = rand_num * 5000000
      self.agents.append(a)

    for i in range(total_poor_agents):
      a = Agent(self.config['agents'])
      a.subtype = "Low"
      rand_num = random.randint(1, 2)
      a.net_worth = rand_num * 10000
      self.agents.append(a)


  def configure_firms(self):
    self.firms = []
    for i in range(self.config['firms']['num_firms']):
      f = Firm(self.config['firms'])
      rand_num = random.randint(1, 101)
      f.money = rand_num * 1000000
      self.firms.append(f)
      # assign random networth between 1B to 100B
    self.track_firm_id = self.firms[0].id

  def configure_regulators(self):
    self.regulators = []  # Might just be a list of 1 item
    for i in range(self.config['regulators']['num_regulators']):
      r = Regulator(self.config['regulators'])
      #rand_num = random.randint(10, 101)
      r.income = 1000000000
      self.regulators.append(r)
      #self.regulators.append(Regulator(self.config['regulators']))

  # ALL decentralized interactions below
  def decentralized_lending(self):
    '''
    Pick a random agent to be the Seeking Agent
    Pick a random agent to be the Lending Agent
    Pick a random interest rate between 1 -> 20% of the Loan Amount
    Pick a random Firm to be the crypto_lending_firm
    Pick a random transaction fee that is between 1 -> 2% of the Loan Amount
    Loan amount gets added to Seeking Agent net worth
    Transaction Fee amount gets subtracted from Seeking Agent's net worth AND added to crypto_lending_firm money
    Interest Rate gets subtracted from Seeking Agent's net worth AND added to Lending Agent net worth
     '''

    seeking_agent = random.choice(self.agents)
    lending_agent = None
    exclude = seeking_agent
    #make sure seeking_agent != lending_agent
    while lending_agent == None or lending_agent == exclude:
      lending_agent = random.choice(self.agents)
    upperBound = np.minimum(0.02 * seeking_agent.net_worth,
                            0.02 * lending_agent.net_worth)
    if upperBound <= 10:
      return
    #setting loan amount
    loan_amount = np.random.randint(0, upperBound)

    #choosing firm that is like blockchain network "provider" - ex/ Ethereum chain
    crypto_lending_firm = random.choice(self.firms)
    #setting transaction fee
    min_transaction_fee = self.get_min_tranaction_fee() * loan_amount
    max_transaction_fee = self.get_max_tranaction_fee() * loan_amount
    transaction_fee = np.random.uniform(min_transaction_fee,
                                        max_transaction_fee)
    crypto_lending_firm.money += transaction_fee
    self.log_firm_money(crypto_lending_firm,"crypto txn fee received")
    seeking_agent.net_worth -= transaction_fee
    #give agent loan money
    seeking_agent.net_worth += loan_amount
    #every iteration, you keep paying the percentage of the loan (interest_rate * loan_amount) back to the lending agent, until the entire loan is paid off
    #seeking_agent.net_worth -= interest_rate
    #lending_agent.net_worth += interest_rate
    self.ledger.initiate_loan(seeking_agent, crypto_lending_firm, loan_amount,
                              lending_agent)

    # scan ledger and randomly pick one loan if any to pay_off, and make interest payment
    # pay interest on loan
    if len(self.ledger.entries) > 5:
      entry = random.choice(self.ledger.entries)
      amount = entry.amount
      #setting interest rate
      min_interest = self.get_min_interest_rate() * amount
      max_interest = self.get_max_interest_rate() * amount
      interest = np.random.uniform(min_interest, max_interest)
      entry.lending_agent.net_worth += interest
      entry.agent.net_worth -= interest
      #print("networth dropping,"+ str(interest))
      #print("loan interest paid" + str(interest))
      # pay off a random loan
      entry = random.choice(self.ledger.entries)
      loan_amount = entry.amount
      entry.firm.money += amount
      self.log_firm_money(entry.firm, "amt received @117")

      entry.agent.net_worth -= amount
      #print("networth dropping,"+ str(amount))

      self.ledger.settle_loan_between_agent_and_agent(entry.agent.id,
                                                      entry.lending_agent.id)

  def interact_agents_with_agents(self):
    """
        1. Randomly pick two agents (people)
        2. Randomly have each of them bet a percentage of their money based on who they are
        3. Have one of the agents win, and take the money, the other lose and lose money

        Policies:
        If netWorth > 500k:
          Invest 40%
          Bet more often @TODO
        Else:
          Invest 10%
          Bet less often @TODO
    """
    agent_win = random.choice(self.agents)
    agents_filtered = []
    for agent in self.agents:
      if ((agent.id != agent_win.id) and (agent.subtype==agent_win.subtype)):
        agents_filtered.append(agent)

    try:
      agent_lose = random.choice(agents_filtered)
    except:
      return

    '''
    #if agent_lose net worth is less than 100 OR if agent_win net worth - agent_lose net worth absolute value is greater than 10000
    if agent_lose.net_worth > 100 or agent_win.net_worth > 100 or np.abs(
        agent_win.net_worth - agent_lose.net_worth) > 10000:
      agent_win = random.choice(self.agents)
      agent_lose = random.choice(self.agents)
    '''

    if agent_lose.net_worth > 500000:
      bet_amount = 0.15 * agent_lose.net_worth
    else:
      bet_amount = 0.02 * agent_lose.net_worth
    #print (">>> bet amount is " + str(bet_amount))

    agent_win.net_worth = agent_win.net_worth + bet_amount
    agent_lose.net_worth = agent_lose.net_worth - bet_amount

    #transaction fee logic to incorporate firms in transactions
    transaction_fee_percentage = np.random.uniform(self.get_min_tranaction_fee(), self.get_max_tranaction_fee())
    transaction_fee = bet_amount * transaction_fee_percentage
    #choose random firm, that is the firm that facilitated the transaction
    handler = random.choice(self.firms)
    handler.money += transaction_fee
    self.log_firm_money(handler, "txn fee received @160")

    agent_win.net_worth -= transaction_fee / 2
    agent_lose.net_worth -= transaction_fee / 2

  def agent_earn_roi(self):
    # if subtype = rich, ROI will be 4%, for middle 3%, and for poor 1% on 50% of networth
    for agent in self.agents:
      if (agent.subtype=="High"):
        roi_rate = self.config["agents"]["roi_rate_high"]
      elif (agent.subtype == "Middle"):
        roi_rate = self.config["agents"]["roi_rate_middle"]
      else:
        roi_rate = self.config["agents"]["roi_rate_low"]

      agent.net_worth += agent.net_worth  * 0.5 * roi_rate


  def interact_firms_with_agents(self):
    """
    interact_firms_with_agents
    1. Agent borrows random number of money from bank (between 100-10,000) - aka a loan - store value in variable 
    "loan"
    2. Every 5 iterations (or some other number), agent "pays interest"
      1. 10% of "loan" is subtracted from agent's networth
      2. 10% of "loan" is added to bank's networth
      Every iteration, 10% is paid off -- but if agent's networth hits 0 before loan is paid off, then that is  defaulting: agent is not allowed to take out more loans
    Bank will not give a loan that exceeds 50 percent of agent's networth AND/OR bank cannot give a loan that exceeds 10% of its net worth
    """
    # create a new loan between a random agent and random firm
    # select a random firm whose total money >= 100
    # if the firm has less than 100 dollars, then skip the loan and make that firm bankrupt and remove it from the list.
    # the actual logic of what should happen to outstanding loans when your bankrupt a firm -- like sell the loans to other firms??
    # for now ..we will just skip the loan

    # Weighted random selection
    firm_weights_raw = np.array([firm.money for firm in self.firms])
    if firm_weights_raw.sum() <= 0 or np.any(firm_weights_raw < 0):
      return  # Return or handle the case where the sum of firm weights is zero or negative or there are negative weights.

    firm_weights = firm_weights_raw / firm_weights_raw.sum()
    if not np.isclose(firm_weights.sum(), 1):
      # Handle the case where the probabilities do not sum up to 1.
      # One option is to renormalize the probabilities:
      firm_weights /= firm_weights.sum()

    agent_firm_choice_index = np.random.choice(range(firm_weights.shape[0]),
                                               p=firm_weights)
    selected_firm = self.firms[agent_firm_choice_index]

    #Fully random selection
    #firm = random.choice(self.firms)
    #if firm.money <= 100:
    #return
    agent = random.choice(self.agents)
    #specify valid loan amount
    upperBound = np.minimum(0.02 * agent.net_worth, 0.02 * selected_firm.money)
    if upperBound <= 10:
      return
    loan_amount = np.random.randint(10, np.maximum(upperBound, 10))

    selected_firm.money = selected_firm.money - loan_amount
    self.log_firm_money(selected_firm, "loand amt deducted @210")

    agent.net_worth = agent.net_worth + loan_amount
    #print ("loan initiated")
    self.ledger.initiate_loan(agent, selected_firm, loan_amount)

    # scan ledger and randomly pick one loan to default, one loan if any to pay_off, and random interest payment
    # pay interest on loan
    if len(self.ledger.entries) > 5:
      entry = random.choice(self.ledger.entries)
      amount = entry.amount
      interest_amount = 0.10 * amount
      entry.firm.money += interest_amount
      self.log_firm_money(entry.firm, "interest amt recieved @222")

      entry.agent.net_worth -= interest_amount
      #print ("loan interest paid")
      # pay off a random loan
      entry = random.choice(self.ledger.entries)
      loan_amount = entry.amount
      entry.firm.money += amount
      self.log_firm_money(entry.firm, "loand amt recieved back @231")

      entry.agent.net_worth -= amount
      self.ledger.settle_loan_between_agent_and_firm(entry.agent.id,
                                                     entry.firm.id)

      # default on a random loan?? firm loses money, what should happen to agent? reduce credit rating? @TODO

  def interact_firms_with_firms(self):
    """
    create new firm (as a combination with another) and get rid of previous 2 -- aka merger
    set fees equal to current and another firm, take that average? (adjusting fees based on other firm fees)
    """

    #mergers and spinoffs
    choice = random.choice([0, 1])
    if choice == 1 and len(self.firms) > 5:
      #merger
      print ("trying to merge 2 firms")
      firm1 = random.choice(self.firms)
      money1 = firm1.money
      firm2 = random.choice(self.firms)
      money2 = firm2.money

      # checking for antitrust rules
      firm_sum = 0
      for firm in self.firms:
        firm_sum += firm.money
      comparison = self.get_merger_threshold() * firm_sum
      if (money1 + money2) < comparison:
        firm2.money += money1
        self.log_firm_money(firm2, "money adjusted post merger @279")
        self.firms.remove(firm1)
        #find out all the loands given out by firm1 and move them to firm2@TODO
        #firm 1 no long exists ..it is now merged with firm2

    if choice == 0:
      #spinoff ie spit a firm into 2
      print ("firms getting split")
      pre_split_firm = random.choice(self.firms)
      moneyBefore = pre_split_firm.money
      new_spinnedoff_firm = Firm(self.config['firms'])
      pre_split_firm.money = moneyBefore / 2
      self.log_firm_money(pre_split_firm, "money halved after split @290")

      new_spinnedoff_firm.money = moneyBefore / 2
      self.log_firm_money(new_spinnedoff_firm, "money halved after split @293")

      self.firms.append(new_spinnedoff_firm)


  def regulators_regulate_firms(self):
    """
     #median, standard dev and mean income of all agents
     #is fee greater than some percentage of that (ex/ 10 %)
     if fees > maxAmount:

     every x iteration, call change_regulations() function

     antitrust: if there is a new firm formed that is the composition, then split that firm back into original
     """
    for item in self.firms:
      money_array = np.array([firm.money for firm in self.firms])
      mean = np.mean(money_array)
      taxRate = self.get_min_tax_rate_firms()
      if item.money >= mean:
        taxRate = self.get_min_tax_rate_firms()
      tax_amount = taxRate * item.money
      reg = random.choice(self.regulators)
      reg.income += tax_amount
      item.money -= tax_amount
      self.log_firm_money(item, "tax payment done @319")

  def regulators_regulate_agents(self):
    """
    every x iteration, call change_regulations() function

    regulator income increases by how much each agent loses (additive)

    1. iterate through all the agents
      1. if agent's income is less than mean, tax rate = 15%
      2. if agent's income is greater than mean, tax rate = 25%
    """
    for item in self.agents:
    #test tax bracket
      money_array = np.array([agent.net_worth for agent in self.agents])
      mean = np.mean(money_array)
      taxRate =self.get_min_tax_rate_agents()
      if item.net_worth >= mean:
        taxRate = self.get_max_tax_rate_agents()
      tax_amount = taxRate * item.net_worth
      item.net_worth = item.net_worth - tax_amount
      reg = random.choice(self.regulators)
      reg.income += tax_amount

  def gov_giving_aid(self):
    """
    Calculate mean
    Min aid is for agents above the poverty line
    Max aid is for agents below the poverty line
    Amount given to high income people = mean * min_gov_aid_agent
    Amount given to low income people = mean * max_gov_aid_agent
    Amount given to high income firms = mean * min_gov_aid_firm
    Amount given to low income firms = mean * max_gov_aid_firm
    **gov_aid_agent (from simulation) is what PERCENTAGE OF THE MEAN each agent will get
    if agents net worth is 25% of the mean, they will get max_gov_aid
    if agents net worth is 50% of the mean, they will get min_gov_aid
    """
    regulator = random.choice(self.regulators)
    net_worth_array = np.array([agent.net_worth for agent in self.agents])
    mean = np.mean(net_worth_array)  # finding net worth
    min_gov_aid_agent = mean * self.get_min_gov_aid_agent()
    max_gov_aid_agent = mean * self.get_max_gov_aid_agent()

    for item in self.agents: #gives money to agents in this scan
      if(item.net_worth <= (0.25 * mean)):
        regulator.income -= max_gov_aid_agent
        item.net_worth += max_gov_aid_agent
      if (item.net_worth <= (0.5 * mean) and item.net_worth > (0.25 * mean)):
        regulator.income -= min_gov_aid_agent
        item.net_worth += min_gov_aid_agent
    #firms
    money_array = np.array([firm.money for firm in self.firms])
    mean = np.mean(money_array)  # finding net worth
    min_gov_aid_firm = mean * self.get_min_gov_aid_firm()
    max_gov_aid_firm = mean * self.get_max_gov_aid_firm()
    for item in self.firms:
      if (item.money <= (0.25 * mean)):
        regulator.income -= max_gov_aid_firm
        item.money += max_gov_aid_firm
      if (item.money <= (0.5 * mean) and item.money > (0.25 * mean)):
        regulator.income -= min_gov_aid_firm
        item.money += min_gov_aid_firm
      self.log_firm_money(item, "aid recieved from govt @381")

  def change_regulatpass(self):
    pass
    """
    "coin flip" -- either increase or decrease tax rate

    run antitrust regulatation or stop it


    # def two_agents_transact(self,
    #   agent1, agent2, transaction):
    #   pass
    
    # def agents_transact(self, agents, transaction):
    #   pass
    
    # def _regulate_agent(self):
    #   pass
    
    # def _regulate_firm(self):
    #   pass
    
    # def _condition_action_space(agent):
    #   new_actions = None
    #   agent.update_action_space(new_actions)
    
    # def regulate(self):
    #   for agent in self.agents:
    #     self._regulate_agent(agent)
    #   for firm in self.firms:
    #     self._regulate_firm(firm)
    
    """

  def save_state(self, current_iteration_count):
    # iterate over all agents and firms and create a simple data structure that can be printed as a csv
    list = self.state
    agent_id = 0
    for agent in self.agents:
      data = {}
      data["Time"] = current_iteration_count
      data["type"] = "agent"
      data["Income-class"] = agent.subtype
      data["id"] = "G" + str(agent_id)
      data["Net-worth"] = "{:.2f}".format(agent.net_worth)
      agent_id = agent_id + 1
      list.append(data)

    firm_id = 0
    for firm in self.firms:
      data = {}
      data["Time"] = current_iteration_count
      data["type"] = "firm"
      data["id"] = "F" + str(firm_id)
      data["Net-worth"] = "{:.2f}".format(firm.money)
      firm_id = firm_id + 1
      list.append(data)

    regulator_id = 0
    for regulator in self.regulators:
      data = {}
      data["Time"] = current_iteration_count
      data["type"] = "regulator"
      data["id"] = "R" + str(regulator_id)
      data["Net-worth"] = "{:.2f}".format(regulator.income)
      regulator_id = regulator_id + 1
      list.append(data)

  def print_state(self, run_number):
    mode = self.config["general"]["mode"]
    regulation = self.config["general"]["regulation_mode"]
    folder_path = mode + "_" + regulation + "_output"
    filename = folder_path+ "/detail_data_iteration" + str(run_number) + ".csv"
    list = self.state

    #write the header of the csv file
    with open(filename, 'w', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=list[0].keys())
      writer.writeheader()

    #write the content of the array to csv file
    with open(filename, 'a', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=list[0].keys())
      for row in list:
        writer.writerow(row)

    summary_data = {}
    summary_data["run"] = run_number
    summary_data["type"] = "agent"
    # create numpy array
    money_array = np.array([agent.net_worth for agent in self.agents])
    max = np.max(money_array)
    summary_data["max"] = max

    min = np.min(money_array)
    summary_data["min"] = min

    median = np.median(money_array)
    summary_data["median"] = median

    mean = np.mean(money_array)
    summary_data["mean"] = mean

    stddev = np.std(money_array)
    summary_data["stddev"] = stddev

    self.summary.append(summary_data)

    print("Agent Stats:")
    print("Min: " + self.formatNumber(min))
    print("Max: " + self.formatNumber(max))
    print("Mean: " + self.formatNumber(mean))
    print("Median: " + self.formatNumber(median))
    print("Std Dev: " + self.formatNumber(stddev))
    print("-------------------------------------------------------")
    print()

    # summary of firms
    summary_data = {}
    summary_data["run"] = run_number
    summary_data["type"] = "firm"

    money_array = np.array([firm.money for firm in self.firms])
    max = np.max(money_array)
    summary_data["max"] = max

    min = np.min(money_array)
    summary_data["min"] = min

    median = np.median(money_array)
    summary_data["median"] = median

    mean = np.mean(money_array)
    summary_data["mean"] = mean

    stddev = np.std(money_array)
    summary_data["stddev"] = stddev

    self.summary.append(summary_data)

    print("Firm Stats:")
    print("Min: " + self.formatNumber(min))
    print("Max: " + self.formatNumber(max))
    print("Mean: " + self.formatNumber(mean))
    print("Median: " + self.formatNumber(median))
    print("Std Dev: " + self.formatNumber(stddev))
    print("# of Firms:" + str(len(self.firms)))
    print("-------------------------------------------------------")
    print()

    #reset the state to None for the next iteration
    self.state = None

  def formatNumber(self, num):
    return str("{:.2f}".format(num))

  def get_merger_threshold(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "merger_threshold_"+regulation_mode
    return self.config["regulators"][key]

  def get_min_tranaction_fee(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "min_transaction_fee_"+regulation_mode
    value = self.config["firms"][key]
    if (self.is_centralized == False):
      value = value *0.5
    return value


  def get_max_tranaction_fee(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "max_transaction_fee_"+regulation_mode
    value = self.config["firms"][key]
    if (self.is_centralized == False):
      value = value *0.5
    return value

  def get_min_tax_rate_agents(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "min_tax_rate_agents_" + regulation_mode
    return self.config["regulators"][key]

  def get_max_tax_rate_agents(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "max_tax_rate_agents_" + regulation_mode
    return self.config["regulators"][key]

  def get_min_tax_rate_firms(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "min_tax_rate_firms_" + regulation_mode
    return self.config["regulators"][key]

  def get_max_tax_rate_firms(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "max_tax_rate_firms_" + regulation_mode
    return self.config["regulators"][key]

  def get_min_interest_rate(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "min_interest_rate_" + regulation_mode
    value = self.config["regulators"][key]
    if (self.is_centralized == False):
      value = value *0.5
    return value

  def get_max_interest_rate(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "max_interest_rate_" + regulation_mode
    value= self.config["regulators"][key]
    if (self.is_centralized == False):
      value = value *0.5
    return value

  def get_min_gov_aid_agent(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "min_gov_aid_agent_" + regulation_mode
    return self.config["regulators"][key]

  def get_max_gov_aid_agent(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "max_gov_aid_agent_" + regulation_mode
    return self.config["regulators"][key]

  def get_min_gov_aid_firm(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "min_gov_aid_firm_" + regulation_mode
    return self.config["regulators"][key]

  def get_max_gov_aid_firm(self):
    regulation_mode = self.config["general"]["regulation_mode"]
    key = "max_gov_aid_firm_" + regulation_mode
    return self.config["regulators"][key]

  def log_firm_money(self,firm, msg):
    pass
    #if firm.id == self.track_firm_id:
     # print(str(firm.money) + ","+ msg)