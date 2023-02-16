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
            v_found = ""
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


def get_meaning_and_example_sentence(word):
    api = ReversoContextAPI(source_text=word, source_lang="de", target_lang="en")

    print("=" * 30)
    for (
        source_word,
        translation,
        frequency,  # how many word usage examples contain this word
        part_of_speech,
        inflected_forms,
    ) in api.get_translations():
        print(source_word, "==", translation)
        break

    for source, target in api.get_examples():
        print(source.text, "==", target.text)
        break

    source_example = source.text
    target_example = target.text
    return translation, source_example, target_example


# It looks promising to get examples but the example method is currently not working: https://github.com/Animenosekai/translate/issues/77#issuecomment-1432278181
# from translatepy import Translator
# from translatepy.translators.bing import BingTranslate
# translate = BingTranslate()

# print(translate.translate("Hello", "German", "English"))
# print(translate.example("Hello", "German", "English"))

from reverso_api.context import ReversoContextAPI

if __name__ == "__main__":
    # Extract vocab
    text = "Berlin ist eine der aufregendsten Städte Europas. Die Hauptstadt Deutschlands bietet eine unvergleichliche Kultur, Geschichte und Architektur. Besucher können durch das Brandenburger Tor spazieren, die Berliner Mauer besichtigen und das berühmte Museuminsel besuchen, um einige der bedeutendsten Kunstwerke der Welt zu sehen. Darüber hinaus gibt es viele Parks, Restaurants und Einkaufsmöglichkeiten für jeden Geschmack. Die Stadt ist bekannt für ihre vielfältige Kunstszene und Nachtleben, das immer pulsierend ist. Berlin ist ein unvergessliches Reiseziel für jeden, der Kultur, Geschichte und Abenteuer erleben möchte."
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)

    vocab_ext = VocabExtractor()

    extracted_vocab = []
    for sentence in doc.sents:
        extracted_vocab.extend(vocab_ext.extract_verbs(sentence))

    print(extracted_vocab)
    for extracted_word in extracted_vocab:

        api = ReversoContextAPI(
            source_text=extracted_word, source_lang="de", target_lang="en"
        )

        print("=" * 30)
        for (
            source_word,
            translation,
            frequency,  # how many word usage examples contain this word
            part_of_speech,
            inflected_forms,
        ) in api.get_translations():
            print(source_word, "==", translation)
            break

        # TODO: select a word meaning according to the context of the paragraph that user entered

        print("Word Usage Examples:")

        for source, target in api.get_examples():
            print(source.text, "==", target.text)
            break

        # TODO: select the sentence according to the word translation selected
