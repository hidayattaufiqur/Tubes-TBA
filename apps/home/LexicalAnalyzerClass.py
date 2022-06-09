import string
import csv

class LexicalAnalyzer:
    def __init__(self, config):
        self.kalimat = config['kalimat']
        self.debug = config['debug']
        self.transisi_lexical = config['transisi_lexical']
        self.input_string = config['kalimat'].lower() + '#'
        self.alphabet_list = list(string.ascii_lowercase)
        self.state_list = []
        self.table_transisi = {}
        self.update_table_transisi = {}
        self.finish_state = ""

        with open(self.transisi_lexical) as file:
            reader = csv.reader(file, delimiter=";")
            
            for kolom in reader:
                state_awal = kolom[0]
                if state_awal not in self.state_list:
                    self.state_list.append(state_awal)
                baca, state_tujuan = kolom[1].split(' ')
                if self.finish_state == '' and state_tujuan == 'accept':
                    self.finish_state = state_awal
                baca = baca.replace("spasi", " ")
                if state_awal == 'q26':
                    self.table_transisi[('q26', "'")] = "q24"

                self.update_table_transisi[(state_awal, baca)] = state_tujuan

        for state in self.state_list:
            for alphabet in self.alphabet_list:
                self.table_transisi[(state, alphabet)] = "error"
            self.table_transisi[(state, "#")] = "error"
            self.table_transisi[(state, " ")] = "error"
        
        for i in self.update_table_transisi:
            self.table_transisi[i] = self.update_table_transisi[i]
            

    def reading(self, Check_L):
        idx_char = 0
        state = "q1"
        current_token = ""

        while state != 'accept' and state != 'error':
            current_char = self.input_string[idx_char]
            current_token += current_char
            state = self.table_transisi[(state, current_char)]

            if (state == self.finish_state) and self.debug:
                print('[VALID] current token:', current_token)
                current_token = ''
            if state == 'error' and self.debug:
                print('[INVALID] current token:', current_token)
                break
            idx_char += 1

        if state == 'accept':
            Check_L = True
            return "[VALID] {}".format(self.kalimat), Check_L
        else:
            Check_L = False
            return "[INVALID] {}".format(self.kalimat), Check_L