# CowBulls Activity
Sugar Activity of the classic "CowBulls" game, with a slight twist ;)

### About:
 - This is a [sugar](https://sugarlabs.org/) activity
 - For instructions on how to play, see [here](INSTRUCTIONS.md)
 - This game has 3 levels
   - Easy (3 Numbers, 5 lives)
   - Medium (4 Numbers, 5 lives)
   - Hard (5 Numbers, 6 lives)
 - Bull overrides cow.
   - Eg: If the correct number is 4864 and you enter 7104, you will get a bull at the last position, and no cow anywhere
 - Correct answer is displayed in case you lose
 - Game can be restarted at any point of time.
 - Your score increases by the number of lives you have + 1


### Development:
 - **Issue/Suggesstion:** If you find an issue or have any suggestions for improvements, please open an issue in the bug tracker.
 - **Contribute:** Contributions(feature/bug-fix) are welcomed. Kindly open a pull request.

### Further Improvements:
 - Option for a two-player shared activity, where one user chooses a number and the other guesses it.
 - Can have numbers coming up until the player loses (A scoring based system, which also saves the high score)
   [IMPLEMENTED in fd2a79]
 - Should have descriptive text at some places in the activity(Depends on initial response of testing)

### Notes:
 - Uses [sugargame](https://github.com/sugarlabs/sugargame) v1.2
 - Adjustable to all Screen sizes

### Known Bugs:
 - Numpad keys 3 and 5 aren't detected.
   Log: `Key KP_Next unrecognised`

### Credits:
 - Thanks to @walterbender, @Hrishi for guiding via irc
 - Icons borrowed from multiple authors via [FlatIcon](https://www.flaticon.com)

### Screenshots:
 - Game won (Level: Medium)
 ![Won difficult](screenshots/en/1.jpg)
 - Game lost (Level: Easy)
 ![Lost medium](screenshots/en/2.jpg)
