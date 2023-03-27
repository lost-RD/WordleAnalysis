from Wordle import Solver, Guess

if __name__ == "__main2__":
    solver = Solver()
    solver.guess(Guess("SALET", "_Y_Y_"))
    solver.guess(Guess("FRAME", "__G_G"))
    solver.guess(Guess("ADAGE", "__G_G"))
    solver.guess(Guess("KNAVE", "_GG_G"))
    solver.guess(Guess("INANE", "GGGGG"))
    solver.evaluate(solution="INANE")

if __name__ == "__main_151122__":
    solution = "MAPLE"
    if True:
        solver = Solver()
        solver.bulk_guess(guesses="""
SALET
LARGE
CABLE
MAPLE
""",
        info="""
⬛🟩🟨🟨⬛
🟨🟩⬛⬛🟩
⬛🟩⬛🟩🟩
🟩🟩🟩🟩🟩
        """)
        solver.evaluate(solution=solution, show_words=True)
    else:
        solver = Solver()
        solver.bulk_guess(guesses="""
STAIN
BAKED
EARLY
MAPLE
""",
        info="""
⬛⬛🟨⬛⬛
⬛🟩⬛🟨⬛
🟨🟩⬛🟩⬛
🟩🟩🟩🟩🟩
        """)
        solver.evaluate(solution=solution, show_words=True)

if __name__ == "__main3__":
    solution = "INANE"
    solver = Solver()
    solver.bulk_guess_without_feedback("""
INCEL
INDIE
INANE
""", solution=solution)
    solver.evaluate(solution=solution, show_words=True)

if __name__ == "__main__":
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