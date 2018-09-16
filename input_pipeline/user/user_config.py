


class UserConfig:

    def __init__(self):
        self.batch_size=10
        self.learning_rate=1.0
        self.recipe="/home/rimhsak/work/nabu/config/recipes/LAS/LIBRI"
        self.expdir="/home/rimhsak/garbage/libri"
        self.train_scp = "/home/rimhsak/work/db/LibriSpeech/libri.sort.train.scp"
        self.train_data_expdir = "/home/rimhsak/garbage/libri/trainfbank"
        self.train_text_data_expdir = "/home/rimhsak/garbage/libri/traintext"

