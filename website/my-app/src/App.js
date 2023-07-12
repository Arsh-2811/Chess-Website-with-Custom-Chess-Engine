import { useState } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";


export default function Board() {
  const [game, setGame] = useState(new Chess());

  const makeMove = (move) => {
    try {
      const result = game.move(move);
      setGame(new Chess(game.fen()));
      return result;
    } catch (error) {
      console.error("Illegal move:", error);
      return null;
    }
}

  function makeRandomMove() {
    const possibleMoves = game.moves();
    if (game.isGameOver() || game.isDraw() || possibleMoves.length === 0) return; // exit if the game is over
    const randomIndex = Math.floor(Math.random() * possibleMoves.length);
    makeMove(possibleMoves[randomIndex]);
  }

  const handleGetMove = async () => {
    try {
      const fen = game.fen();
      const response = await fetch('http://127.0.0.1:8000/get-move', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fen: fen,
          depth: 2, // specify your desired depth here
        }),
      });
  
      if (response.ok) {
        const newFen = await response.json();
        console.log(newFen)
        setGame(new Chess(newFen));
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };


  function onDrop(sourceSquare, targetSquare) {
    const move = makeMove({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q", // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return false;
    
    setTimeout(handleGetMove, 20000);
    return true;
  }
  
  return(
     <div>
        <Chessboard 
        boardWidth={600}
          arePiecesDraggable = {true}
          position={game.fen()} 
          onPieceDrop={onDrop} 
        />
     </div>
  )
}