from enum import Enum
import math

EMOJI_BLANK = "⬛"
EMOJI_YELLOW = "🟨"
EMOJI_GREEN = "🟩"

class Info(Enum):
    BLANK = 0
    YELLOW = 1
    GREEN = 2

WORDS = []
with open("words", "r") as file:
    for line in file:
        WORDS.append(line.rstrip().lower())

class Letter:
    
    def __init__(self, position: int, letter: str, info: str, guess: int) -> None:
        self.position = position
        self.letter = letter.lower()
        match info:
            case "_": info = Info.BLANK
            case "Y": info = Info.YELLOW
            case "G": info = Info.GREEN
            case "⬛": info = Info.BLANK
            case "🟨": info = Info.YELLOW
            case "🟩": info = Info.GREEN
        self.info: Info = info
        self.guess = guess
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Letter):
            return False
        return all([self.info == __o.info,
                   self.letter == __o.letter,
                   self.position == __o.position,
                   self.guess == __o.guess])
    
    def __hash__(self) -> int:
        letter_int = ord(self.letter) - 96
        info_int = 10 * self.info.value
        pos_int = 100 * self.position
        guess_int = 1000 *  self.guess
        return letter_int + info_int + pos_int + guess_int
    
    def __str__(self) -> str:
        info = "X"
        match self.info:
            case Info.BLANK: info = EMOJI_BLANK
            case Info.YELLOW: info = EMOJI_YELLOW
            case Info.GREEN: info = EMOJI_GREEN
        return f"{self.guess}:{self.letter.upper()}@{self.position}|{info}"
    
    def __repr__(self) -> str:
        return str(self)

class Guess:
    next_guess = 1
    
    def __init__(self, word: str, information: str, guess_number: int = None) -> None:
        self.word = word.lower()
        self.information = information
        if guess_number is not None:
            self.guess_number = guess_number
        else:
            self.guess_number = Guess.next_guess
            Guess.next_guess += 1
        self.letters: list[Letter] = []
        for i in range(0,5):
            letter, info = word[i], information[i]
            letter = Letter(i, letter, info, self.guess_number)
            self.letters.append(letter)

class Solver:
    
    def __init__(self) -> None:
        self.words = WORDS.copy()
        self.information: set[Letter] = set()
        self.guesses: list[Guess] = []
    
    def guess(self, guess: Guess) -> None:
        #print(guess.word, guess.guess_number, guess.information, ", ".join([str(letter) for letter in guess.letters]))
        for letter in guess.letters:
            self.information.add(letter)
        self.guesses.append(guess)
    
    def guess_without_feedback(self, word: str, solution: str):
        info = self.calculate_info(word, solution)
        guess = Guess(word, info)
        self.guess(guess)
    
    def list_words_remaining(self, up_to_guess: int = 6) -> list[str]:
        words: list[str] = self.words.copy()
        words.sort()
        current_guess = 1
        valid_information = set(letter for letter in self.information if letter.guess <= up_to_guess)
        #iterations = 1
        while (information := set([letter for letter in valid_information if letter.guess == current_guess])):
            #print(information, iterations)
            #iterations += 1
            guess_word = self.guesses[current_guess-1].word
            
            blanks = [letter for letter in information if letter.info == Info.BLANK]
            yellows = [letter for letter in information if letter.info == Info.YELLOW]
            greens = [letter for letter in information if letter.info == Info.GREEN]
            
            if len(greens) > 0:
                for letter_green in greens:
                    words = [word for word in words if word[letter_green.position] == letter_green.letter]

            if len(yellows) > 0:
                for letter_yellow in yellows:
                    words = [word for word in words if word[letter_yellow.position] != letter_yellow.letter]
                    words = [word for word in words if letter_yellow.letter in word]
            
            if len(blanks) > 0:
                for letter_blank in blanks:
                    other_appearances = [letter.letter for letter in yellows if letter.letter == letter_blank.letter] + [letter.letter for letter in greens if letter.letter == letter_blank.letter]
                    if len(other_appearances) == 0:
                        words = [word for word in words if letter_blank.letter not in word]
                    else:
                        words = [word for word in words if word.count(letter_blank.letter) <= len(other_appearances)]

            current_guess += 1
            words = [word for word in words if word != guess_word]
        words.sort()
        return words
    
    def num_words_remaining(self, up_to_guess: int = 6) -> int:
        return len(self.list_words_remaining(up_to_guess=up_to_guess))
    
    def bulk_guess(self, guesses: str = None, info: str = None):
        guesses = guesses.lstrip().rstrip().splitlines()
        info = info.lstrip().rstrip().splitlines()
        assert len(guesses) == len(info), "Lines of guesses and information must match"
        for i in range(0, len(guesses)):
            self.guess(Guess(guesses[i], info[i]))

    def bulk_guess_without_feedback(self, guesses: str, solution: str):
        guesses = guesses.lstrip().rstrip().splitlines()
        for i in range(0, len(guesses)):
            self.guess_without_feedback(guesses[i], solution)
    
    def calculate_info(self, word_guessed: str, solution: str):
        word_guessed, solution = word_guessed.lower(), solution.lower()
        info = ""
        for i in range(0, 5):
            guessed_letter = word_guessed[i]
            actual_letter = solution[i]
            if guessed_letter == actual_letter:
                info += EMOJI_GREEN
                solution = list(solution)
                solution[i] = "_"
                solution = "".join(solution)
            elif guessed_letter in solution:
                j = solution.find(guessed_letter)
                info += EMOJI_YELLOW
                solution = list(solution)
                solution[j] = "_"
                solution = "".join(solution)
            else:
                info += EMOJI_BLANK
        return info
    
    def evaluate(self, solution: str = None, show_words: bool = False):
        solution = solution.lower()
        score = 0
        total_entropy = math.log(self.num_words_remaining(up_to_guess=0), 2)
        assert solution is not None, "Must provide parameter solution"
        guesses = max(self.information, key=lambda x: x.guess).guess
        print(f"Guesses used: {guesses}")
        solved = self.guesses[-1].word.lower() == solution.lower()
        print(f"Solved: {'yes' if solved else 'no'}")
        words_remaining_prior = len(self.words)
        entropy_prior = total_entropy
        
        for i in range(0, guesses):
            print("")
            guess_num = i+1
            print(f"Guess {guess_num}")
            guess = [guess for guess in self.guesses if guess.guess_number == guess_num][0]
            print(f"Guessed: {''.join([str(char)+' ' for char in guess.word]).upper()}")
            info = guess.information.replace("_", "⬛").replace("G", "🟩").replace("Y", "🟨")
            print(f"Info:    {info}")
            words_remaining_now = self.list_words_remaining(up_to_guess=guess_num)
            
            num_words_remaining_now = len(words_remaining_now)
            if guess.word == solution:
                num_words_remaining_now = 0
                score += entropy_prior
            print(f"Words remaining: {num_words_remaining_now}", end="")
            if num_words_remaining_now > 0:
                entropy_now = math.log(num_words_remaining_now, 2)
                print(f" (down from {words_remaining_prior})")
                information = entropy_prior-entropy_now
                score += information*(6-i)/6
                print(f"Information: {information:0.2f} bits (of {entropy_prior:0.2f})")
                
                if guess_num > 0 and solution is not None:
                    words_remaining_before = self.list_words_remaining(up_to_guess=guess_num-1)
                    entropies = []
                    for word in words_remaining_before:
                        hypothetical_solver = self.copy(max_guess=guess_num-1)
                        info_from_word = self.calculate_info(word, solution)
                        
                        hypothetical_solver.guess(Guess(word, info_from_word, guess_number=guess_num))
                        hypothetical_words_remaining_now = hypothetical_solver.list_words_remaining()
                        
                        if len(hypothetical_words_remaining_now) > 0:
                            hypothetical_entropy_now = math.log(len(hypothetical_words_remaining_now), 2)
                            hypothetical_information = entropy_prior - hypothetical_entropy_now
                        else:
                            hypothetical_information = entropy_prior
                        
                        if word != solution:
                            entropies.append((word, hypothetical_information))
                    
                    if len(entropies) > 0:
                        entropies.sort(key=lambda x: x[1], reverse=True)
                        best_entropy = entropies[0][1]
                        best_words = [t[0] for t in entropies if t[1] == best_entropy]
                        print(f"Maximum info available: {best_entropy: >5.2f} bits from:  {', '.join(best_words).upper()}")
                        if show_words:
                            words_to_show = self.list_words_remaining(up_to_guess=guess_num)
                            max_num_words_to_show = 32
                            if len(words_to_show) > max_num_words_to_show:
                                print("Remaining words:     "+", ".join(words_to_show[0:max_num_words_to_show]).upper()+", ...")
                            else:
                                print("Remaining words:     "+", ".join(words_to_show).upper())
            else:
                print("\nSolved!")
                score = 100 * score / total_entropy
                print(f"Score: {score:.1f}")
                return
            words_remaining_prior, entropy_prior = num_words_remaining_now, entropy_now
    
    def copy(self, max_guess=6):
        copy: Solver = Solver()
        for guess in self.guesses:
            if guess.guess_number <= max_guess:
                copy.guess(guess)
        return copy