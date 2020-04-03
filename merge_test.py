import spacy

nlp = spacy.load("en_core_web_sm")

print("without merging ...")
test_text = nlp("I have a blue car.")
for token in test_text:
    print(token, token.dep_, token.pos_)

print()
print("with merging ...")
merge_nps = nlp.create_pipe("merge_noun_chunks")
merge_ents = nlp.create_pipe("merge_entities")
merge_subtok = nlp.create_pipe("merge_subtokens")
nlp.add_pipe(merge_nps)
nlp.add_pipe(merge_ents)
nlp.add_pipe(merge_subtok)

test_text = nlp("I have a blue car.")
for token in test_text:
    print(token, token.dep_, token.pos_)
