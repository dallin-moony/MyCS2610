import { useState, useEffect } from 'react';
import Key from './key';
import Phrase from './phrase';

const quotes = [
    "Ask not what your country can do for you, ask what you can do for your country. - John F. Kennedy",
    "The only thing we have to fear is fear itself. - Franklin D. Roosevelt",
    "In the end, it's not the years in your life that count. It's the life in your years. - Abraham Lincoln",
    "Do what you can, with what you have, where you are. - Theodore Roosevelt",
    "I came, I saw, I conquered. - Julius Caesar",
    "Discipline is the soul of an army. - George Washington",
    "Victory belongs to the most persevering. - Napoleon Bonaparte",
    "The best way to predict your future is to create it. - Peter Drucker",
    "If you want peace, prepare for war. - Vegetius",
    "A house divided against itself cannot stand. - Abraham Lincoln",
    "Great spirits have always encountered violent opposition from mediocre minds. - Albert Einstein",
    "The supreme art of war is to subdue the enemy without fighting. - Sun Tzu",
    "The harder the conflict, the greater the triumph. - George Washington",
    "Imagination is more important than knowledge. - Albert Einstein",
    "Courage is being scared to death, but saddling up anyway. - John Wayne",
    "It always seems impossible until it's done. - Nelson Mandela",
    "To be prepared for war is one of the most effectual means of preserving peace. - George Washington",
    "The buck stops here. - Harry S. Truman",
    "Injustice anywhere is a threat to justice everywhere. - Martin Luther King Jr.",
    "If everyone is thinking alike, then somebody isn't thinking. - George S. Patton",
    "Efforts and courage are not enough without purpose and direction. - John F. Kennedy",
    "A leader is one who knows the way, goes the way, and shows the way. - John C. Maxwell",
    "You miss 100% of the shots you don't take. - Wayne Gretzky",
    "Wars are won by the great strength of a nation's spirit. - Douglas MacArthur",
    "I have not failed. I've just found 10,000 ways that won't work. - Thomas Edison",
    "Those who dare to fail miserably can achieve greatly. - John F. Kennedy",
    "Do not pray for easy lives. Pray to be stronger men. - John F. Kennedy",
    "Never interrupt your enemy when he is making a mistake. - Napoleon Bonaparte",
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit. - Aristotle",
    "Perseverance and spirit have done wonders in all ages. - George Washington"
];

const baseKeys = [
['1','2','3','4','5','6','7','8','9','0','-','='],
['q','w','e','r','t','y','u','i','o','p','[',']'],
['a','s','d','f','g','h','j','k','l',';',"'"],
['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
[' ']
];

const shiftMap = {
'1':'!',
'2':'@',
'3':'#',
'4':'$',
'5':'%',
'6':'^',
'7':'&',
'8':'*',
'9':'(',
'0':')',
'q':'Q',
'w':'W',
'e':'E',
'r':'R',
't':'T',
'y':'Y',
'u':'U',
'i':'I',
'o':'O',
'p':'P',
'[':'{',
']':'}',
'a':'A',
's':'S',
'd':'D',
'f':'F',
'g':'G',
'h':'H',
'j':'J',
'k':'K',
'l':'L',
';':':',
"'":'"',
'z':'Z',
'x':'X',
'c':'C',
'v':'V',
'b':'B',
'n':'N',
'm':'M',
',':'<',
'.':'>',
'/':'?',
'-':'_',
'=':'+',
' ':' ',
'Shift':'Shift'
};

function Keyboard() {
    const [isShifted, setIsShifted] = useState(false);
    // use null as the "no key pressed" sentinel so it doesn't collide with empty-string labels
    const [pressedKeys, setPressedKeys] = useState(new Set());
    const [currentPhrase, setPhrase] = useState(0);
    const [currentLetter, setLetter] = useState(0);
    const correctLetter = quotes[currentPhrase][currentLetter];

    /*Note to self: useEffect is a side effect hook that will happen on render. The [] at the end means it will render only once*/


    useEffect(() => {
        const handleKeyPress = (e) => {
            if (e.repeat) return;
            if (e.key === 'Shift') {
                setIsShifted(true);
            }
            if (e.key === correctLetter) {
                setLetter((prev) => prev + 1);
                if (currentLetter + 1 === quotes[currentPhrase].length) {
                    setPhrase((prev) => (prev + 1) % quotes.length);
                    setLetter(0);
                }
            }
            setPressedKeys((prev) => {
                const newPressed = new Set(prev);
                newPressed.add(e.key);
                return newPressed;
            });
        };

        const handleKeyUpPress = (e) => {
            if (e.key === 'Shift') {
                setIsShifted(false);
            }
            setPressedKeys((prev) => {
                const newPressed = new Set(prev)
                newPressed.delete(e.key);
                return newPressed;
            });
        };

        window.addEventListener('keydown', handleKeyPress);
        window.addEventListener('keyup', handleKeyUpPress);
        return () => {
            window.removeEventListener('keydown', handleKeyPress);
            window.removeEventListener('keyup', handleKeyUpPress);
        };
    }, [ correctLetter, currentLetter, currentPhrase]);

    return (
        <div className="app">
            <Phrase quotes={quotes} currentPhrase={currentPhrase} currentLetter={currentLetter} />
            <div className="keyboard">
                {baseKeys.map((row, rowIndex) => (
                    <div key={rowIndex} className="key-row">
                        {row.map((keyLabel, keyIndex) => {
                            const renderedLabel = isShifted ? (shiftMap[keyLabel] ?? keyLabel) : keyLabel;
                            console.log(pressedKeys);
                            const isDown = pressedKeys.has(renderedLabel);
                            const isNext = renderedLabel === correctLetter;
                            let className = isDown ? 'pressed' : isNext ? 'next-key' : '';
                            const needsShift = !baseKeys.flat().includes(correctLetter);
                            if (renderedLabel === 'Shift' && needsShift) {
                                className += ' next-key';
                            }
                            return <Key key={keyIndex} label={renderedLabel} className={className} />;
                        })}
                    </div>
                ))}
            </div>
        </div>
    );
}
export default Keyboard;