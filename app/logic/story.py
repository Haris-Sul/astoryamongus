class Story:
    def __init__(self):
        self.story_text = ""
        self.sentences = []

    def add_sentence(self, author, sentence):
        self.story_text += sentence + "\n"
        self.sentences.append(f"{author}: {sentence}")
