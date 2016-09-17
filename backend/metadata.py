
class Metadata:

    def __init__(self, filename="metadata.txt"):

        metadata_file = open(filename, 'r')

        self.patent_to_tags = {}
        self.tags_to_patent = {}
        for line in metadata_file:
            patent, cat, state = line.split()
            self.patent_to_tags[patent] = (cat, state)
            if cat in self.tags_to_patent:
                self.tags_to_patent[cat].append(patent)
            else:
                self.tags_to_patent[cat] = [patent]

            if state in self.tags_to_patent:
                self.tags_to_patent[state].append(patent)
            else:
                self.tags_to_patent[state] = [patent]

    def getPatentsInCategory(self, cat):
        return self.tags_to_patent[cat]

    def getPatentsInState(self, state):
        return self.tags_to_patent[state]

    def getPatentTags(self, patent):
        if self.hasMetadata(patent):
            return self.patent_to_tags[patent]
        else:
            return (-1, -1)

    def hasMetadata(self, patent):
        return patent in self.patent_to_tags
