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
        verbs_found = []
        for token in sentence:
            v_found = ''
            if token.pos_ != "VERB":
                continue

            # check infinitive form
            if token.tag_ == "VVINF":
                v_found = token.text
                verbs_found.append(v_found)
                continue

            v_found = self.check_reflexive_verb(token)
            if v_found:
                verbs_found.append(v_found)
                continue

            v_found = self.check_separable_verb(token)
            if v_found:
                verbs_found.append(v_found)
                continue

            #  conjugated: should not be placed before reflexive and separable
            if token.tag_ in ["VVIZU", "VVPP", "VVFIN"]:
                v_found = token.lemma_
                verbs_found.append(v_found)
        return verbs_found


nlp = spacy.load("de_core_news_sm")
doc = nlp("Berlin ist eine der aufregendsten Städte Europas. Die Hauptstadt Deutschlands bietet eine unvergleichliche Kultur, Geschichte und Architektur. Besucher können durch das Brandenburger Tor spazieren, die Berliner Mauer besichtigen und das berühmte Museuminsel besuchen, um einige der bedeutendsten Kunstwerke der Welt zu sehen. Darüber hinaus gibt es viele Parks, Restaurants und Einkaufsmöglichkeiten für jeden Geschmack. Die Stadt ist bekannt für ihre vielfältige Kunstszene und Nachtleben, das immer pulsierend ist. Berlin ist ein unvergessliches Reiseziel für jeden, der Kultur, Geschichte und Abenteuer erleben möchte.")

# doc = nlp("Sie hat sich gestern Abend ausgespannt")

vocab_ext = VocabExtractor()

for sentence in doc.sents:
    print(vocab_ext.extract_verbs(sentence))
