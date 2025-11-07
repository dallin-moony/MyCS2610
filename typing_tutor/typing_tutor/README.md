# Project Requirements
1. A phrase shown at the top of the screen. 
    * Font color/size updates when the correct letter is typed. When phrase is completed a new phrase is displayed in the view.
    * Incorrect letters do not do anything to the phrase. Delete, enter, tab, and control do not appear on the screen and do not do anything.
    * Caps lock will not change the appearance of the keyboard. It DOES however still change the actual input of the keyboard. E.g. if you have caps lock on, you will need to hold shift to type a lowercase letter, but the keyboard will appear capitalized. In this case it's best to hope/assume that caps lock is not pressed as it throws off the whole program.
2. Keyboard shown in the middle of the screen.
    * Keyboard buttons respond when the corresponding key is pressed.
    * Next correct key is highlighted (shadow)
        * This includes the shift key. It will be highlighted if the next letter is capitalized or if it is a symbol that requires the shift key to be held. It will then highlight the correct (capitalized) key.
    * Keyboard updates to capitalized keys and symbols when the shift key is pressed.
    * Multiple keys can be pressed
