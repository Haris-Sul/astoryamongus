import random
class StoryGenerator:
    def __init__(self):
        self.templates = [
            "Once upon a time, in a land filled with {}...",
            "The adventure began in a {} forest where mysterious things happened.",
            "The kingdom of {} was known for its incredible legends.",
            "In the {} mountains, a brave hero faced many challenges.",
            "A {} storm turned the peaceful village upside down."
        ]

    def generate(self, keyword):
        """Generate the first part of the story based on the keyword."""
        if not keyword:
            return "No keyword provided."
        template = random.choice(self.templates)
        return template.format(keyword)