# Loads a corpus of sentences in typedbytes format from Hadoop into a database.

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


import typedbytes
from ratings.models import *

file = open("/Users/pealco/archive/experiments/disagreement/data.tb", 'rb')
input = typedbytes.PairedInput(file)

for sha1, sentence in input:

    s = Sentence(
        sha1=sha1,
        sentence=sentence.sentence,
        grammatical=sentence.grammatical,
        similarity=sentence.wup_similarity
    )
    s.save()

    dg = DirectedGraph()
    dg.save()

    nodelist = [Node() for node in sentence.dg.nodelist]
    [node.save() for node in nodelist]

    subject_address = sentence.subject['address']
    intervenor_address = sentence.intervenor['address']
    verb_address = verb.intervenor['address']

    for node in sentence.dg.nodelist:
        current_node = node['address']

        n = nodelist[current_node]

        # Attributes.
        n.address = node['address']
        n.word = node['word']
        n.tag = node['tag']
        n.rel = node['rel']

        # Pointers at other nodes.
        n.subject = nodelist[subject_address]
        n.intervenor = nodelist[intervenor_address]
        n.verb = nodelist[verb_address]

        # List of dependent nodes.
        for dep in node['deps']:
            n.deps.add(nodelist[dep])

        # The first node never has a head.
        try:
            head = node['head']
        except KeyError:
            continue
        n.head = nodelist[head]

        # Save the node.
        n.save()

        # Add the node to the current directed graph.
        dg.nodes.add(n)

    dg.save()

    s.dg = dg
    s.save()
