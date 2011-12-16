from django.db import models


class Node(models.Model):
    head    = models.ForeignKey("self", blank=True, null=True)
    word    = models.CharField(blank=True, max_length=30)
    rel     = models.CharField(blank=True, max_length=10)
    tag     = models.CharField(blank=True, max_length=10)
    deps    = models.ManyToManyField("self", symmetrical=False, related_name="dependencies")
    address = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.word


class DirectedGraph(models.Model):
    nodes = models.ManyToManyField(Node)


class Sentence(models.Model):

    RATING_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('?', 'Not sure'),
    )
    
    sha1        = models.CharField(max_length=40)
    sentence    = models.CharField(max_length=500)
    dg          = models.ForeignKey(DirectedGraph, blank=True, null=True)
    subject     = models.ForeignKey(Node, blank=True, null=True, related_name="subj")
    intervenor  = models.ForeignKey(Node, blank=True, null=True)
    grammatical = models.BooleanField(default=True)
    similarity  = models.FloatField(blank=True, null=True)
    rel_freq    = models.IntegerField(blank=True, null=True)
    rating      = models.CharField(blank=True, max_length=1, choices=RATING_CHOICES)
    
    def __unicode__(self):
        return self.sentence
