import numpy as np
import six

from .data_flow import Dataflow


class BatchData(Dataflow):
    """
    make batch-sized data
    """

    def __init__(self, dataflow, batch_size, remainder=False):
        """
        :param dataflow: dataflow
        :param batch_size: batch size
        :param remainder:
            if False, generagtes a batch to have data as same as batch_size
            if True, is able to generate a batch to have less data than batch_size
        """
        super(BatchData, self).__init__(dataflow)
        self.dataflow = dataflow
        self.batch_size = int(batch_size)
        self.remainder = remainder
        self.is_stop = False

    def reset(self):
        pass

    def get_data(self):
        """
        :return: batched data
        """
        holder = []
        for data in self.dataflow.get_data():
            if self.is_stop is True:
                break
            print("in bath get data %s"%data[1])
            holder.append(data)
            if len(holder) == self.batch_size:
                #print("len(holder): %d" % len(holder))
                yield BatchData._aggregate_batch(holder)
                del holder[:]
        if self.remainder and len(holder) > 0:
            yield BatchData._aggregate_batch(holder)

    @staticmethod
    def _aggregate_batch(data_holder):
        size = len(data_holder)
        print("in aggregate_bath, size: %d"%size)

        # data, label
        # for data
        datas = np.zeros([size, len(data_holder[0][0])])
        for i in range(size):
            #print("in aggregate_bath %s" % data_holder[i][0])
            data = data_holder[i][0]
            if type(data) in list(six.integer_types) + [bool]:
                tp = 'int32'
            elif type(data) == float:
                tp = 'float32'
            else:
                try:
                    tp = data.dtype
                except AttributeError:
                    raise TypeError("Unsupport type to batch: {}".format(type(data)))
            try:
                datas[i] = np.asarray(data, dtype=tp)
            except Exception as e:
                print("Cannot batch data {}".format(str(e)))

        # for data
        labels = np.zeros([size, len(data_holder[0][1])])
        for i in range(size):
            print("in aggregate_bath %s" % data_holder[i][1])
            label = data_holder[i][1]
            if type(label) in list(six.integer_types) + [bool]:
                tp = 'int32'
            elif type(label) == float:
                tp = 'float32'
            else:
                try:
                    tp = label.dtype
                except AttributeError:
                    raise TypeError("Unsupport type to batch: {}".format(type(data)))
            try:
                labels[i] = np.asarray(label, dtype=tp)
            except Exception as e:
                print("Cannot batch data {}".format(str(e)))

            """
            if user_list_flag is True:
                result.append([x[i] for x in data_holder])
            else:
                print(data_holder[0][1])
                print(i)
                data = data_holder[0][i]
                if type(data) in list(six.integer_types) + [bool]:
                    tp = 'int32'
                elif type(data) == float:
                    tp = 'float32'
                else:
                    try:
                        tp = data.dtype
                    except AttributeError:
                        raise TypeError("Unsupport type to batch: {}".format(type(data)))

                try:
                    result.append(
                        np.asarray([x[i] for x in data_holder], dtype=tp))
                except Exception as e:
                    print("Cannot batch data {}".format(str(e)))
            """

        return (datas, labels)

    def stop(self):
        self.is_stop = True

    def __del__(self):
        self.is_stop = True
    










