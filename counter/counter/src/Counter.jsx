import { useState } from "react";

export function Counter() {
    const [count, setCount] = useState(0);

    function increment() {
        setCount(count + 1);
    }
    function decrement() {
        setCount(count - 1);
    }
    function double() {
        setCount(count * 2);
    }
    function halve() {
        setCount(count / 2);
    }   
    function increment5() {
        setCount(count + 5);
    }
    function decrement5() {
        setCount(count - 5);
    }
    return (
        <body>
            <div className="counter">
                <h1>Count: {count}</h1>
                <div>
                    <button onClick={decrement}>-</button>
                    <button onClick={increment}>+</button>
                </div>
                <div>
                    <button onClick={decrement5}>-5</button>
                    <button onClick={increment5}>+5</button>
                </div>
                <div>
                    <button onClick={halve}>Halve</button>
                    <button onClick={double}>Double</button>
                </div>
                <button onClick={() => setCount(0)}>Reset</button>
            </div>
        </body>
    );
}