#!/usr/bin/env python


class Group:
    xindex = 0
    yindex = 1
    windex = 2
    lindex = 3
    def __init__(self,label):
        self.label = label
        self.members = []

        self.update_cg()

    @staticmethod
    def get_default_cg():
        cg = [None,None,None,None]
        cg[Group.xindex] = 0
        cg[Group.yindex] = 0
        cg[Group.windex] = 1
        cg[Group.lindex] = 'Unknown'
        return cg

    def add_member(self,member):
        self.members.append(member)
        self.update_cg()

    def add_members(self,members):
        self.members.extend(members)
        self.update_cg()

    def update_cg(self):
        total_weight = sum( [ m[Group.windex] for m in self.members ] )
        size = len(self.members) * 1.0

        if size == 0:
            self.cg = Group.get_default_cg()
        else:
            self.cg[Group.windex] = total_weight / size
            self.cg[Group.xindex] = sum( [ m[Group.xindex] * m[Group.windex] for m in self.members ]  ) / size
            self.cg[Group.yindex] = sum( [ m[Group.yindex] * m[Group.windex] for m in self.members ]  ) / size
            self.cg[Group.lindex] = self.label

    def __repr__(self):
        return "%s { x : %s, y : %s, weight : %s }" % (
                self.cg[Group.lindex],
                self.cg[Group.xindex],
                self.cg[Group.yindex],
                self.cg[Group.windex])

    def square_distance(self,entity):
        dx = ( (entity[Group.xindex] * entity[Group.windex]) - (self.cg[Group.xindex] * self.cg[Group.windex]) )
        dy = ( (entity[Group.yindex] * entity[Group.windex]) - (self.cg[Group.yindex] * self.cg[Group.windex]) )

        return (dx*dx + dy*dy)


class CenterGravityClassifier:
    def __init__(self):
        self.groups = {}

    def add_entity(self,entity):
        label = entity[Group.lindex]

        if label not in self.groups:
            g = Group(label)
            self.groups[label] = g

        self.groups[label].add_member(entity)

    def add_entities(self,entities):
        if len(entities) == 0:
            return

        labels = set([ e[Group.lindex] for e in entities ])

        for label in labels:
            if label not in self.groups:
                g = Group(label)
                self.groups[label] = g

            lentities = filter(lambda e: e[Group.lindex] == label, entities)

            self.groups[label].add_members(lentities)

    def predict_group(self,entity):
        if len(self.groups) == 0:
            return None

        return min(self.groups.values(), key=lambda g:g.square_distance(entity))


if __name__ == '__main__':
    train = [
            [2, 4, 1, 'male'],
            [3, 5, 1, 'male'],
            [15, 14, 1, 'female'],
            [13,15, 1, 'female'],
            ]
    test = [4,3,1,None]

    cg_classifier = CenterGravityClassifier()

    cg_classifier.add_entities(train)

    prediction = cg_classifier.predict_group(test)

    print "Given training DataSet: \r\n %s" % train
    print "*" * 20
    print "For entity : %s" % test
    print "*" * 20
    print "Center of Gravity Classifier classification:\r\n"
    print "---- this item belongs to the Group with Center of Gravity: %s" %  prediction
    print "**** Thus we label it '%s'" % prediction.label
