# WordleAnalysis

Inspired by WordleBot, which was free but now is not. Replicates some of WordleBot's functionality.

Not optimised, exhaustively searches and takes >30 seconds to run.

Works on the assumption that all guessable words are valid answers, which we know to be false, but working from the answers list from the original Wordle release doesn't leave us with much to work with. A better list might be a more conservative dictionary that contains all of the original answers.

# How It Works

## Sample Input

```
info = """
🟩🟨🟨⬛⬛
🟩⬛🟩⬛🟩
🟩🟩🟩⬛🟩
🟩🟩🟩🟩🟩
"""
guesses = """
SALET
SHALL
SNAIL
SNARL
"""
solution = "SNARL"
solver = Solver()
solver.bulk_guess(
    guesses=guesses,
    info=info
)
solver.evaluate(solution=solution, show_words=True)
```

## Sample Output

```
Guesses used: 4
Solved: yes

Guess 1
Guessed: S A L E T
Info:    🟩🟨🟨⬛⬛
Words remaining: 49 (down from 14855)
Information: 8.24 bits (of 13.86)
Maximum info available: 13.86 bits from:  ANILS, LARNS, NIRLS, NURLS, ROSAL, SERAL, SLAIN, SLART, SNAIL, SORAL, SURAL
Remaining words:     SCAIL, SCALA, SCALD, SCALL, SCALP, SCALY, SHALL, SHALM, SHALY, SHAUL, SHAWL, SHOAL, SHOLA, SIALS, SIGLA, SISAL, SKAIL, SKALD, SKOAL, SLABS, SLACK, SLAGS, SLAID, SLAIN, SLAMS, SLANG, SLANK, SLAPS, SLASH, SLAWS, SLAYS, SLOAN, ...

Guess 2
Guessed: S H A L L
Info:    🟩⬛🟩⬛🟩
Words remaining: 9 (down from 49)
Information: 2.44 bits (of 5.61)
Maximum info available:  5.61 bits from:  SLAIN, SNAIL, SORAL, SURAL
Remaining words:     SCAIL, SKAIL, SNAIL, SNARL, SPAIL, SPAUL, SPAWL, SWAIL, SWAYL

Guess 3
Guessed: S N A I L
Info:    🟩🟩🟩⬛🟩
Words remaining: 1 (down from 9)
Information: 3.17 bits (of 3.17)
Maximum info available:  3.17 bits from:  SNAIL
Remaining words:     SNARL

Guess 4
Guessed: S N A R L
Info:    🟩🟩🟩🟩🟩
Words remaining: 0
Solved!
Score: 89.4
```
