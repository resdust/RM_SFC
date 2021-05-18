from network_env import Env
import sqlite3

class Service():
    def __init__(self,number,sequence):
        conn = sqlite3.connect('data/nfv.sqlite')
        self.number = number
        self.sequence = sequence
        self._insert(conn)

    def _insert(self,conn):
        insert = 'REPLACE INTO service '

def actionTransfer():
    env = Env()

    action_total = env.action_total
    action_services = {}
    sequences = []
    services = []

    for state in action_total:
        actions = action_total[state]
        action_services[state] = []
        for action in actions:
            if action not in sequences:
                sequences.append(action)
            no = sequences.index(action)
            action_services[state].append(no)

    for seq in sequences:
        service = Service(sequences.index(seq),seq)
        services.append(service)

    return action_services

if __name__=="__main":
    actions = actionTransfer()

    