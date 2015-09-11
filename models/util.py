
import pickle

def load_pickle(file_):
    if isinstance(file_, str):
        with open(file_, 'r') as f:
            return pickle.load(f)
    else:
        return pickle.load(file_)

def save_pickle(file_, data):
    if isinstance(file_, str):
        with open(file_, 'w') as f:
            return pickle.dump(date, f, pickle.HIGHEST_PROTOCOL)
    else:
        return pickle.dump(date, file_, pickle.HIGHEST_PROTOCOL)
