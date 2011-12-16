class Sentence(object):

    def __init__(self, article, dg):
        
        self.punct_re = re.compile(r'\s([,\.;\?])')

        self.dg = dg    
        self.sentence = self._plaintext()
        self.subject = self._find_subject()
        self.intervenor = self._find_intervenor()
        self.grammatical = self._find_grammaticality()
        self.wup_similarity = self._wup_similarity()
        
    def _plaintext(self):
        s = " ".join([node["word"] for node in self.dg.nodelist[1:]])
        return re.sub(self.punct_re, r'\g<1>', s)
    
    def wup_similarity(self):
        """Compute Wu-Palmer similarity."""
        try:
            subject_synset = wn.synsets(self.subject)[0]
            intervenor_synset = wn.synsets(self.intervenor)[0]
            similarity = subject_synset.wup_similarity(intervenor_synset)
            return similarity
        except:
            return None
    
    def _find_intervenor(self):
        
        subject_deps = self.subject[0]['deps']
        prepositions = [self.dg.get_by_address(dep) for dep in subject_deps if self.dg.get_by_address(dep)['tag'] == 'IN']
        try:
            first_prep = prepositions[0]
            intervenor = self.dg.get_by_address(first_prep['deps'][0])
        except IndexError:
            return None
        
        return intervenor
    
    def _root_dependencies(self, dg): 
        return [dg.get_by_address(node) for node in dg.root["deps"]]
    
    def _dependencies(dg, node): 
        return [dg.get_by_address(dep) for dep in dg.get_by_address(node["address"])["deps"]]
    
    def _find_subject(self):
        return [node for node in self._root_dependencies(self.dg) if node["rel"] == "SBJ"]
    
    def _find_grammaticality(self):
        subject_tag = self.subject[0]["tag"]
        verb = self.dg.root
        verb_tag = self.dg.root["tag"]
    
        if subject_tag in NUMBER and verb_tag in NUMBER:
            if NUMBER[subject_tag] == NUMBER[verb_tag]:
                return True
            elif NUMBER[subject_tag] != NUMBER[verb_tag]:
                return False
    
    def __str__(self):
        return self.sentence