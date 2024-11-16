class Story:
    def __init__(self):
        self.sentences = []

    def add_sentence(self, author, sentence):
        self.sentences.append(f"{author}: {sentence}")

    def get_full_story(self):
        return "\n".join(self.sentences)
