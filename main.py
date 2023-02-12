#  tags explanation:  https://www.sketchengine.eu/german-stts-part-of-speech-tagset/
import spacy
from spacy.lang.de.examples import sentences

nlp = spacy.load("de_core_news_sm")
doc = nlp("Ich hatte mich gewaschen")
print(doc.text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
    if token.pos_ != "VERB":
        continue

    if token.tag_ == "VVINF":  # infinitive form
        print("infinitive")
        print(token.text)
        continue

    if token.tag_ in [
        "VVIZU",  #  Infinitiv mit "zu"e.g anzukommen
        "VVPP",  # past participle of full verb e.g gekommt
    ]:
        print("Infinitiv mit zu")
        print(token.lemma_)
        continue

    # import pdb; pdb.set_trace()
    if token.tag_ == "VVFIN":
        separable_verb_conjugated = ""
        reflexive = ""

        for child in token.children:
            if (
                child.pos_ == "ADP" and child.tag_ == "PTKVZ"
            ):  # separable verb conjugated
                separable_verb_conjugated = child.text + token.text

            if child.tag_ == "PRF":
                reflexive = f"sich {token.lemma_}"
                # print(reflexive)

        if separable_verb_conjugated or reflexive:
            print(separable_verb_conjugated)
            print(reflexive)
        else:  # conjugated
            print("conjugated")
            print(token.lemma_)
