class TestPhrase:

    def test_len_phrase(self):
        phrase = input("Set a phrase: ")

        assert len(phrase) < 15, f"Phrase more than 15 symbols"
