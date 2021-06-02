from network_env import Env
import sqlite3
import sys

class Service():
    def __init__(self,number,sequence):
        conn = sqlite3.connect('data/nfv.sqlite')
        self.number = number
        self.sequence = sequence
        self._insert(conn)

    def _insert(self,conn):
        insert = 'INSERT OR IGNORE INTO service (service_id, vnf_id, next_vnf_id) VALUES (?,?,?)'
        sequence = self.sequence
        cur = conn.cursor()

        for i in range(len(sequence)):
            service_id = str(self.number+1)
            vnf_id = str(sequence[i]+1)
            next_vnf_id = None
            if i != len(sequence)-1:
                next_vnf_id = str(sequence[i+1]+1)
            cur.execute(insert,(service_id,vnf_id,next_vnf_id))
        conn.commit()

    def execute(self):
        add_command = "curl -v http://127.0.0.1:8080/add_flow/{}"
        del_command = "curl -v http://127.0.0.1:8080/delete_flow/{}"

        number = self.number
        sequences = self.sequence

        # for seq in range(1,5):
        #     sys.execute(del_command.format(seq))

        # for seq in sequences:
        sys.execute(add_command.format(number))
    
    def delete(self):
        del_command = "curl -v http://127.0.0.1:8080/delete_flow/{}"
        number = self.number
        sys.execute(del_command.format(number))

def actionTransfer():
    env = Env()

    action_total = env.action_total
    action_num = 0
    action_services = {} # int -> [], action -> services No.s
    sequences = []
    services = []

    for state in action_total:
        actions = action_total[state]
        for action in actions:
            action_services[action_num] = []
            for flow in action:
                if flow not in sequences:
                    sequences.append(flow)
                no = sequences.index(flow)
                action_services[action_num].append(no) 
            action_num = action_num+1

    for seq in sequences:
        service = Service(sequences.index(seq),seq)
        services.append(service)

    return action_services,services


if __name__=="__main__":
    actions,services = actionTransfer()
    