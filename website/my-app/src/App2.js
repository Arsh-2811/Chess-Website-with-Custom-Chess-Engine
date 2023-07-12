import { useState } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";
import "./App.css"

export default function Board() {
  const [game, setGame] = useState(new Chess());

  function onDragStart (piece, sourceSquare){
    if(game.isGameOver()) return false;
    if(piece.search(/^b/) !== -1) return false;    //Only pick up pieces for white 
  }

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
          depth: 4, // specify your desired depth here
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





  



  const [moveFrom, setMoveFrom] = useState("");
  const [rightClickedSquares, setRightClickedSquares] = useState({});
  const [moveSquares, setMoveSquares] = useState({});
  const [optionSquares, setOptionSquares] = useState({});

  function getMoveOptions(square) {
    const moves = game.moves({
      square,
      verbose: true,
    });
    if (moves.length === 0) {
      return false;
    }
    const newSquares = {};
    moves.map((move) => {
      newSquares[move.to] = {
        background:
          game.get(move.to) && game.get(move.to).color !== game.get(square).color
            ? "radial-gradient(circle, rgba(0,0,0,.1) 85%, transparent 85%)"
            : "radial-gradient(circle, rgba(0,0,0,.1) 25%, transparent 25%)",
        borderRadius: "50%",
      };
      return move;
    });
    newSquares[square] = {
      background: "rgba(255, 255, 0, 0.4)",
    };
    setOptionSquares(newSquares);
    return true;
  }

  function onSquareClick(square) {
    setRightClickedSquares({});
    function resetFirstMove(square) {
      const hasOptions = getMoveOptions(square);
      if (hasOptions) setMoveFrom(square);
    }
    // from square
    if (!moveFrom) {
      resetFirstMove(square);
      return;
    }

    // attempt to make move
    const move = makeMove({
        from: moveFrom,
        to: square,
        promotion: "q", // always promote to a queen for example simplicity
      });

    // if invalid, setMoveFrom and getMoveOptions
    if (move === null) {
      resetFirstMove(square);
      return;
    }

    setTimeout(handleGetMove, 20000);
    setMoveFrom("");
    setOptionSquares({});
  }
  
  function onSquareRightClick(square) {
    const colour = "rgba(0, 0, 255, 0.4)";
    setRightClickedSquares({
      ...rightClickedSquares,
      [square]:
        rightClickedSquares[square] &&
        rightClickedSquares[square].backgroundColor === colour
          ? undefined
          : { backgroundColor: colour },
    });
  }

  return(
     <div>
        <Chessboard 
          boardWidth={600}
          arePiecesDraggable = {false}
          animationDuration={200}
          position={game.fen()} 
        //   onPieceDrop={onDrop} 
        //   onPieceDragBegin={onDragStart}
          onSquareClick={onSquareClick}
          onSquareRightClick={onSquareRightClick}
          customSquareStyles={{
            ...moveSquares,
            ...optionSquares,
            ...rightClickedSquares,
          }}

          customBoardStyle={{
            borderRadius: "4px",
            boxShadow: "0 2px 10px rgba(0, 0, 0, 0.5)",
          }}
          customDarkSquareStyle={{ backgroundColor: "#779952" }}
          customLightSquareStyle={{ backgroundColor: "#edeed1" }}
        />
        <button
        className="button"
        onClick={() => {
          game.reset();
          setMoveSquares({});
          setRightClickedSquares({});
        }}
      >
        reset
      </button>
     </div>
  )
}