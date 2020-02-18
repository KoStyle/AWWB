import pickle

from constants import ACCESS_TOKENS_DIC


class InputKun:

    @staticmethod
    def read_file(file):
        lista = []
        try:
            f = open(file, 'r', encoding='latin1')
        except:
            f = open(file, 'w+', encoding='latin1')
        line = f.readline()
        while line:
            lista.append(line.strip())
            line = f.readline()
        return lista

    @staticmethod
    def read_tokens(file):
        f = open(file, 'r', encoding='latin1')
        line = f.readline()
        while line:
            tokenized = line.split('=')
            if ACCESS_TOKENS_DIC.get(tokenized[0].strip()) is None and len(tokenized) == 2:
                ACCESS_TOKENS_DIC[tokenized[0].strip()] = tokenized[1].strip()
            line = f.readline()
        return

    @staticmethod
    def load_pickle(file):
        f = open(file, 'rb')
        listaObj = pickle.load(f)
        f.close()
        return listaObj

    @staticmethod
    def save_pickle(file, obj):
        f = open(file, 'wb')
        pickle.dump(obj, f)
        f.close()
