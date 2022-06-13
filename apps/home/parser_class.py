import csv


class Parser:
    def __init__(self, config):
        '''initialize'''
        self.kalimat = config['kalimat']
        self.parse_table_file = config['parse_table']
        self.debug = config['debug']
        self.token = self.kalimat.lower().split()
        self.token.append('EOS')
        self.non_terminal_list = []
        self.terminal_list = []
        self.parse_table = {}

        with open(self.parse_table_file) as file:
            reader = csv.reader(file, delimiter=',')

            for idx, val in enumerate(reader):
                if idx == 0:
                    self.terminal_list = val[1:-1]
                else:
                    for i, v in enumerate(val[1:-1]):
                        if len(v.split(' ')) > 0:
                            self.parse_table[(
                                val[0], self.terminal_list[i])] = v.split(' ')
                        else:
                            self.parse_table[(val[0], self.terminal_list[i])] = [v]

                    self.non_terminal_list.append(val[0])

    def reading(self, Check_P):
        stack = ['#', 'S']
        idx_token = 0
        simbol = self.token[idx_token]

        while(len(stack) > 0 and simbol in self.terminal_list):
            top = stack[len(stack)-1]
            if self.debug:
                print('[TOP]', top)
                print('[simbol]', simbol)
            if top in self.terminal_list and top == simbol:
                if self.debug:
                    print('FOUND - Terminal')
                stack.pop()
                idx_token += 1
                simbol = self.token[idx_token]
                if simbol == 'EOS':
                    if self.debug:
                        print('[ISI]', stack)
                    stack.pop()
            elif top in self.non_terminal_list and self.parse_table[(top, simbol)][0] != 'error':
                if self.debug:
                    print('FOUND - Non terminal')
                stack.pop()
                simbol_to_be_pushed = self.parse_table[(top, simbol)]
                for i in range(len(simbol_to_be_pushed)-1, -1, -1):
                    stack.append(simbol_to_be_pushed[i])
            else:
                break

            if self.debug:
                print('[STACK]', stack)

        if simbol == 'EOS' and len(stack) == 0:
            Check_P = True
            return 'ACCEPT - {} sesuai dengan grammar'.format(self.kalimat), Check_P
        else:
            Check_P = False
            return 'ERROR - {} tidak sesuai dengan grammar'.format(self.kalimat), Check_P