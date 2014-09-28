from mrjob.job import MRJob


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        yield {'k': 'chars'}, len(line)
        yield {'k': 'words'}, len(line.split())
        yield {'k': 'lines'}, 1

    def reducer(self, key, values):
        yield key['k'], sum(values)


if __name__ == '__main__':
    MRWordFrequencyCount.run()
