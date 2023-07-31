#  tags explanation:  https://www.sketchengine.eu/german-stts-part-of-speech-tagset/
import spacy
from wordfreq import zipf_frequency
from reverso_api.context import ReversoContextAPI


class VocabExtractor:
    def __init__(self) -> None:
        pass

    def check_reflexive_verb(self, token):
        reflexive = ""

        if token.tag_ in [
            "VVIZU",  #  Infinitiv mit "zu"e.g anzukommen
            "VVPP",  # past participle of full verb e.g gekommt
            "VVFIN",  # conjugated
            "VVINF" # infinitive sich anmelden, sich enscheiden
        ]:
            for child in token.children:
                if child.tag_ == "PRF":
                    reflexive = f"sich {token.lemma_}"
                    break
        return reflexive

    def check_separable_verb(self, token):
        separable = ""
        # import pdb; pdb.set_trace()
        if token.tag_ in ["VVFIN"]:  # conjugated
            for child in token.children:
                if (
                    child.pos_ == "ADP" and child.tag_ == "PTKVZ"
                ):  # separable verb conjugated
                    separable = child.text + token.lemma_
        return separable

    def extract_vocab(self, sentence):
        vocab_found = []
        for token in sentence:
            
            # check adjective
            # if token.pos_ == "ADJ":
            #     vocab_found.append(token.lemma_)
            #     continue

            # continue if not verb
            if token.pos_ != "VERB":
                continue

            

            v_found_reflexive = self.check_reflexive_verb(token)
            
            
        

            v_found_separable = self.check_separable_verb(token)
            # import pdb; pdb.set_trace()
            
            if v_found_reflexive and v_found_separable:
                # import pdb; pdb.set_trace()
                vocab_found.append(f"sich {v_found_separable}")
                continue
            
            elif v_found_reflexive:
                v_found_reflexive.split()[-1]
                vocab_found.append(v_found_reflexive)
                continue
            elif v_found_separable:
                # import pdb; pdb.set_trace()
                vocab_found.append(v_found_separable)
                continue
            
            # check infinitive form
            if not v_found_reflexive and token.tag_ == "VVINF":
                v_found = token.text
                vocab_found.append(v_found)
                continue

            #  conjugated: should not be placed before reflexive and separable
            if token.tag_ in ["VVIZU", "VVPP", "VVFIN"]:
                v_found = token.lemma_
                vocab_found.append(v_found)
        return vocab_found

    def check_token_status(self, token, token_status_threhold):
    
        token_text = token
        token_freq = zipf_frequency(token_text, 'de', wordlist='best') # [1, 8]

        if token_freq == 0:
            token_status = "not_found"
        elif token_freq > token_status_threhold: # easy word
            token_status = "easy"
        else:
            token_status = "hard"

        return token_status




  


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



if __name__ == "__main__":
    
    # Extract vocab
    text = "Ich werde heute ein neues Auto kaufen"
    
    # text = "Der Zug fährt pünktlich um vier Uhr ab."

    # text = "Das Hotel befindet sich an einem kleinen See."
    # text = "Die Branche hat sich in den letzten Jahren rapide entwickelt."

    # # text = "Ich habe mich zu einem Sprachkurs angemeldet."

    

    # text = "Ich muss mich anstrengen, um die gesamte Arbeit rechtzeitig zu erledigen."
    

    # text = "Berlin ist eine der aufregendsten Städte Europas. Die Hauptstadt Deutschlands bietet eine unvergleichliche Kultur, Geschichte und Architektur. Besucher können durch das Brandenburger Tor spazieren, die Berliner Mauer besichtigen und das berühmte Museuminsel besuchen, um einige der bedeutendsten Kunstwerke der Welt zu sehen. Darüber hinaus gibt es viele Parks, Restaurants und Einkaufsmöglichkeiten für jeden Geschmack. Die Stadt ist bekannt für ihre vielfältige Kunstszene und Nachtleben, das immer pulsierend ist. Berlin ist ein unvergessliches Reiseziel für jeden, der Kultur, Geschichte und Abenteuer erleben möchte."
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)



    vocab_ext = VocabExtractor()

    extracted_vocab = [] 
    for sentence in doc.sents:
        extracted_vocab.extend(vocab_ext.extract_vocab(sentence))

    print(extracted_vocab)
    import pdb; pdb.set_trace()
    
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
