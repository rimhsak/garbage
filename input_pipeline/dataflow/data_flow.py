from user.user_config import UserConfig
from user.user_trainer import UserTrainer


class Dataflow(object):

    def __init__(self, user_trainer):
        self._user_trainer = user_trainer

    def reset(self):
        """
        initialize dataflow
        it is a simple wrapper of the part of data in UserTrainer
        :return: none
        """
        self._user_trainer.InitData()

    def get_data(self):
        """
        get data from dataflow, which is defined by users
        it is a simple wrapper of the part of data in UserTrainer
        :return: data
        """

        return self._user_trainer.GetData()

    def transform_data(self, data):
        """
        transform pure data to augmented data
        it is a simple wrapper of the part of data in UserTrainer
        :return: transformed data
        """

        return self._user_trainer.TransformData(data)

    def get_mode(self):
        return self._user_trainer.GetMode()


class AugmentedDataflow(Dataflow):

    def __init__(self, user_trainer):
        super(AugmentedDataflow, self).__init__(self)
        self._user_trainer = user_trainer

    def reset(self):
        """
        initialize dataflow
        it is a simple wrapper of the part of data in UserTrainer
        :return: none
        """
        self._user_trainer.InitData()

    def get_data(self):
        """
        get data from dataflow, which is defined by users
        it is a simple wrapper of the part of data in UserTrainer
        :return: data
        """
        data = self._user_trainer.GetData()
        return self._user_trainer.TransformData(data)

    def transform_data(self, data):
        """
        transform pure data to augmented data
        it is a simple wrapper of the part of data in UserTrainer
        :return: transformed data
        """

        return self._user_trainer.TransformData(data)

    def get_mode(self):
        return self._user_trainer.GetMode()




