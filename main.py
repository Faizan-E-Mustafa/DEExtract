#  tags explanation:  https://www.sketchengine.eu/german-stts-part-of-speech-tagset/
import spacy


class VocabExtractor:
    def __init__(self) -> None:
        pass

    def check_reflexive_verb(self, token):
        reflexive = ""

        if token.tag_ in [
            "VVIZU",  #  Infinitiv mit "zu"e.g anzukommen
            "VVPP",  # past participle of full verb e.g gekommt
            "VVFIN",  # conjugated
        ]:
            for child in token.children:
                if child.tag_ == "PRF":
                    reflexive = f"sich {token.lemma_}"
                    break
        return reflexive

    def check_separable_verb(self, token):
        separable = ""

        if token.tag_ in ["VVFIN"]:  # conjugated
            for child in token.children:
                if (
                    child.pos_ == "ADP" and child.tag_ == "PTKVZ"
                ):  # separable verb conjugated
                    separable = child.text + token.text
        return separable

    def extract_verbs(self, sentence):
        for token in sentence:
            if token.pos_ != "VERB":
                continue

            # check infinitive form
            if token.tag_ == "VVINF":
                verb_found = token.text
                return verb_found

            verb_found = self.check_reflexive_verb(token)
            if verb_found:
                return verb_found

            verb_found = self.check_separable_verb(token)
            if verb_found:
                return verb_found

            #  conjugated: should not be placed before reflexive and separable
            if token.tag_ in ["VVIZU", "VVPP", "VVFIN"]:
                verb_found = token.lemma_
                return verb_found



nlp = spacy.load("de_core_news_sm")
doc = nlp(
    "Ich hoffe, dass ich rechtzeitig anzukommen werde, um den Anfang der Konferenz nicht zu verpassen"
)

doc = nlp("Sie hat sich gestern Abend ausgespannt")

{   "KOKOM":"comparative conjunction",
    "KON": "coordinate conjunction",
    "KOUI": 'subordinate conjunction with "zu" and infinitive',
    "KOUS": "subordinate conjunction with sentence"}

clauses = []
for sent in doc.sents:
    clause_start_idx = 0
    for clause_end_idx, token in enumerate(sent):
       
        if token.tag_ in ["KOKOM", "KON", "KOUI", "KOUS"]:
            
            clauses.append(sent[clause_start_idx:clause_end_idx])
            clause_start_idx = clause_end_idx

    clauses.append(sent[clause_start_idx:])

    

vocab_ext = VocabExtractor()

for clause in clauses:
    print(clause)
    
    print(vocab_ext.extract_verbs(clause))

