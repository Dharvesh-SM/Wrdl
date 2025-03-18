import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Add CSS for square boxes

// Use Production API URL
const API_BASE = "https://wrdl.onrender.com";

function App() {
  const [word, setWord] = useState("");
  const [guess, setGuess] = useState("");
  const [message, setMessage] = useState("");
  const [guesses, setGuesses] = useState([]);
  const [attempts, setAttempts] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  // Fetch the target word on page load
  useEffect(() => {
    getWord();
  }, []);

  // Get new word from Flask backend
  const getWord = async () => {
    try {
      const response = await axios.get(`${API_BASE}/word`);
      setWord(response.data.word);
      resetGame();
    } catch (error) {
      console.error("Error fetching word:", error);
    }
  };

  // Reset the game
  const resetGame = () => {
    setMessage("Start guessing!");
    setGuesses([]);
    setAttempts(0);
    setGameOver(false);
    setGuess("");
  };

  // Check the guessed word with hints
  const checkGuess = async () => {
    if (gameOver || guess.length !== word.length) return;

    try {
      const response = await axios.post(`${API_BASE}/check`, {
        word: guess,
      });

      setMessage(response.data.message);

      // Add guess and hints to the list
      setGuesses([
        ...guesses,
        { guess: guess.toUpperCase(), hints: response.data.hints },
      ]);

      if (response.data.valid) {
        setGameOver(true);
      } else {
        const newAttempts = attempts + 1;
        setAttempts(newAttempts);

        if (newAttempts >= 6) {
          setGameOver(true);
          setMessage(`Game over! The correct word was: ${word.toUpperCase()}`);
        }
      }

      setGuess("");
    } catch (error) {
      console.error("Error checking guess:", error);
    }
  };

  // Restart the game by fetching a new word
  const restartGame = async () => {
    try {
      const response = await axios.get(`${API_BASE}/restart`);
      setWord(response.data.word);
      resetGame();
    } catch (error) {
      console.error("Error restarting game:", error);
    }
  };

  return (
    <div className="container">
      <h1>Wordle Clone</h1>
      <p>{message}</p>

      {/* Show all guesses with hints */}
      <div className="grid">
        {guesses.map((entry, i) => (
          <div key={i} className="row">
            {entry.guess.split("").map((char, j) => (
              <div
                key={j}
                className={`box ${
                  entry.hints[j] === "🟩"
                    ? "green"
                    : entry.hints[j] === "🟨"
                    ? "yellow"
                    : "gray"
                }`}
              >
                {char}
              </div>
            ))}
          </div>
        ))}

        {/* Show empty rows for remaining attempts */}
        {[...Array(6 - guesses.length)].map((_, i) => (
          <div key={`empty-${i}`} className="row">
            {[...Array(word.length)].map((_, j) => (
              <div key={j} className="box empty"></div>
            ))}
          </div>
        ))}
      </div>

      {!gameOver && (
        <>
          <input
            type="text"
            value={guess}
            onChange={(e) => setGuess(e.target.value.toUpperCase())}
            maxLength={word.length}
            className="input-box"
          />
          <button onClick={checkGuess} className="btn-check">
            Check
          </button>
        </>
      )}

      {gameOver && (
        <button onClick={restartGame} className="btn-restart">
          Restart Game
        </button>
      )}

      <p>Attempts: {attempts}/6</p>
    </div>
  );
}

export default App;
