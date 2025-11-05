function Phrase({ quotes, currentPhrase, currentLetter }) {
    return (
        <div className="phrases">
            <div className="phrase">
                {quotes[currentPhrase].split("").map((char, index) => (
                    <span
                        key={index}
                        className={
                            index < currentLetter
                                ? "correct"
                                : index === currentLetter
                                ? "current"
                                : ""
                        }
                    >
                        {char}
                    </span>
                ))}
            </div>
        </div>
    );
}

export default Phrase;