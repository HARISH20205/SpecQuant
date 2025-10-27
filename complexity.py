import nltk
from nltk import word_tokenize, pos_tag, ne_chunk, sent_tokenize


class ComplexityLevels:
    high: str = "high"
    mid: str = "med"
    low: str = "low"


class ClassifyPrompt:
    def __init__(self, prompt: str):
        # nltk.download('punkt') 
        # nltk.download('averaged_perceptron_tagger')
        # nltk.download('maxent_ne_chunker')
        # nltk.download('words')
        # nltk.download('punkt_tab')
        # nltk.download('averaged_perceptron_tagger_eng')
        # nltk.download('maxent_ne_chunker_tab')
        self.prompt = prompt
        self.tokens = word_tokenize(prompt)
        self.pos_tags = pos_tag(self.tokens)
        self.ner_tree = ne_chunk(self.pos_tags)
    
    def __call__(self):
        return self.final_complexity()

    def length_complexity(self):
        length = len(self.prompt.split())
        if length <= 7:
            length_complexity = ComplexityLevels.low
        elif 8 <= length <= 15:
            length_complexity = ComplexityLevels.mid
        else:
            length_complexity = ComplexityLevels.high

        return length_complexity

    def semantic_complexity(self):
        entity_count = sum(1 for chunk in self.ner_tree if hasattr(chunk, 'label'))

        if entity_count  <= 1:
            ner_complexity = ComplexityLevels.low
        elif entity_count == 2:
            ner_complexity = ComplexityLevels.mid
        else:
            ner_complexity = ComplexityLevels.high

        return ner_complexity
    
    def syntactic_complexity(self):
        conj_count = sum(1 for _, tag in self.pos_tags if tag in {'CC'})  # Conjunctions
        sub_clause_count = sum(1 for _, tag in self.pos_tags if tag in {'IN', 'TO'})  # Subordinate clauses

        sentences = sent_tokenize(self.prompt)
        num_sentences = len(sentences)
        avg_sentence_length = len(self.tokens) / num_sentences if num_sentences > 0 else 0

        complexity_score = (
            conj_count + sub_clause_count + (1 if avg_sentence_length > 12 else 0)
        )

        if complexity_score <= 1:
            return ComplexityLevels.low
        elif complexity_score == 2:
            return ComplexityLevels.mid
        else:
            return ComplexityLevels.high
        
    def final_complexity(self):
        length_comp = self.length_complexity()

        semantic_comp = self.semantic_complexity()

        syntactic_comp = self.syntactic_complexity()

        length_score = 0 if length_comp == ComplexityLevels.low else (2 if length_comp == ComplexityLevels.mid else 4)
        semantic_score = 0 if semantic_comp == ComplexityLevels.low else (2 if semantic_comp == ComplexityLevels.mid else 4)
        syntactic_score = 0 if syntactic_comp == ComplexityLevels.low else (2 if syntactic_comp == ComplexityLevels.mid else 4)
        print(f"Length: {length_comp}, Semantic: {semantic_comp}, Syntactic: {syntactic_comp}")
        total_score = length_score*1 + semantic_score*2 + syntactic_score*3

        if total_score <= 3:
            return  ComplexityLevels.low
        elif 4 <= total_score <= 8:
            return  ComplexityLevels.mid
        else:
            return  ComplexityLevels.high
    @staticmethod
    def get_complexity(prompt: str):
        classifier = ClassifyPrompt(prompt)
        return classifier.final_complexity()


example_prompts = {
    "low": [
        "What is AI?",
        "Define gravity.",
        "Who is the president?",
        "List three colors.",
        "What is Python?"
    ],
    "mid": [
        "Explain the process of photosynthesis.",
        "How does a car engine work?",
        "Describe the water cycle in brief.",
        "What are the benefits of exercise?",
        "Summarize the plot of Romeo and Juliet."
    ],
    "high": [
        "Analyze the impact of climate change on global agriculture and suggest mitigation strategies.",
        "Compare and contrast machine learning and deep learning with examples.",
        "Discuss the ethical implications of artificial intelligence in healthcare.",
        "Evaluate the effectiveness of renewable energy sources in reducing carbon emissions.",
        "Explain the process of DNA replication and its significance in genetic inheritance."
    ]
}

if __name__ == "__main__":
    for complexity_level, prompts in example_prompts.items():
        for prompt in prompts:
            complexity = ClassifyPrompt.get_complexity(prompt)
            print(f" Prompt: {prompt}\nPrompt Complexity Level: {complexity}\n\n")
