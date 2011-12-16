from django.http import HttpResponse
from django.template import Context

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ratings.models import *

import rpy2.robjects as robjects
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects.packages import importr


def main(request):

    sentence = Sentence.objects.filter(grammatical=False, rating="").order_by("?")[0]

    gram = {
        "yes":      len(Sentence.objects.filter(grammatical=True, rating="Y")),
        "no":       len(Sentence.objects.filter(grammatical=True, rating="N")),
        "notsure":  len(Sentence.objects.filter(grammatical=True, rating="?")),
        "unrated":  len(Sentence.objects.filter(grammatical=True, rating="")),
    }

    ungram = {
        "yes":      len(Sentence.objects.filter(grammatical=False, rating="Y")),
        "no":       len(Sentence.objects.filter(grammatical=False, rating="N")),
        "notsure":  len(Sentence.objects.filter(grammatical=False, rating="?")),
        "unrated":  len(Sentence.objects.filter(grammatical=False, rating="")),
    }

    variables = Context({
        'gram': gram,
        'ungram': ungram,
        'sentence': sentence,
    })
    return render_to_response('main.html', variables)


def rate(request, id, rating):
    s = Sentence.objects.get(pk=id)

    ratings = {
        'yes':    'Y',
        'no':     'N',
        'notsure': '?',
    }

    try:
        s.rating = ratings[rating]
    except:
        pass

    s.save()

    return HttpResponseRedirect(reverse(main))


def plot(request):
    r = robjects.r

    ungram = Sentence.objects.filter(grammatical=False).exclude(rating='N').values_list('similarity', flat=True)
    gram = Sentence.objects.filter(grammatical=True).exclude(rating='N').values_list('similarity', flat=True)

    gram_r = robjects.FloatVector(gram)
    ungram_r = robjects.FloatVector(ungram)

    df = robjects.r["data.frame"]
    gram_df = df(gram="GRAM", similarity=gram_r)
    ungram_df = df(gram="UNGRAM", similarity=ungram_r)

    rbind = r['rbind']
    data = rbind(gram_df, ungram_df)

    pp = ggplot2.ggplot(data) + \
        ggplot2.aes_string(x="gram", y="similarity") + \
        ggplot2.geom_boxplot()

    grdevices = importr('grDevices')
    grdevices.png(file="data.png", width=580, height=512)
    pp.plot()
    grdevices.dev_off()

    image_data = open("data.png", "rb").read()

    return HttpResponse(image_data, mimetype="image/png")


def compute_similarity(pair):
    subject, intervener = pair

    try:
        subject_synset = wn.synsets(subject)[0]
        intervener_synset = wn.synsets(intervener)[0]
        similarity = subject_synset.wup_similarity(intervener_synset)
        return similarity
    except:
        return False
