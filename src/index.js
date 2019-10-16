import React, { useState, useEffect, useCallback } from 'react';
import ReactDOM from 'react-dom';
import 'json-loader';
import './index.css';


function Square(props) {
  if (!props.ifEnd) {
    return (
      <button
        className="square"
        style={{background: props.color}}
        onClick={props.onClick}
      />
    )
  }
  else {
    return (
      <div
        className="squarediv"
        style={{background: "white"}}
      >
        <button
          className="circle"
          style={{background: props.color}}
          onClick={props.onClick}
        />
      </div>
    )
  }
}

function Game(props) {
  // having these as props prevents bugs due to re-renders
  const ends = props.ends;
  const setEnds = props.setEnds;
  const [nextColor, setnextColor] = useState('white');
  const currSq = props.currSq;
  const setCurrSq = props.setCurrSq;
  const [boardDisplay, setBoardDisplay] = useState([]);
  const response = props.response;
  const setLoaded = props.setLoaded;
  const loaded = props.loaded;
  const boardSqs = props.boardSqs;
  const setboardSqs = props.setboardSqs;
  let numNotEnds = props.numNotEnds;

  useEffect(() => {
    getBoard(response);
  }, []);

  const getBoard = (input) => {
    console.log('getting board');
    let colorArray = [];
    let endArray = [];
    for (let i = 0; i < input.board.length; i++) {
      let thisRow = input.board[i];
      // allows for boards of different shapes and sizes
      colorArray.push([]);
      endArray.push([]);
      for (let j = 0; j < thisRow.length; j++) {
        if (thisRow[j].length > 1) {
          endArray[i].push(true);
          switch (thisRow[j]) {
            case 'rr':
              colorArray[i].push('red');
              break;
            case 'oo':
              colorArray[i].push('orange');
              break;
            case 'gg':
              colorArray[i].push('green');
              break;
            case 'yy':
              colorArray[i].push('yellow');
              break;
            case 'bb':
              colorArray[i].push('blue');
              break;
            case 'cc':
              colorArray[i].push('cyan');
              break;
            case 'pp':
              colorArray[i].push('purple');
              break;
            case 'mm':
              colorArray[i].push('maroon');
              break;
            default:
            // should not do this, means there is an error
              colorArray[i].push('pink');
          }
        }
        else {
          colorArray[i].push('white');
          endArray[i].push(false);
        }
      }
    };
    setboardSqs(colorArray);
    setEnds(endArray);
  }

  // memoizing the board
  useEffect(() => {
    let board = [];

    for (let i = 0; i < boardSqs.length; i++) {
      let children = [];
      for (let j = 0; j < boardSqs.length; j++) {
        children.push(<Square
                        key={(i.toString() + j.toString())}
                        color={boardSqs[i][j]}
                        ifEnd={ends[i][j]}
                        onClick={() => {
                          let temp = [i, j];
                          setCurrSq(temp);
                        }}
                      />);
        if (!ends[i][j]) numNotEnds++;
      }
      board.push(<div
                  className="board-row"
                  key={i.toString()}>
                  {children}
                 </div>)
    }
    setBoardDisplay(board);
    setLoaded(true);
  }, [boardSqs])

  // this hook handles clicks - changes the board when the currSq changes
  useEffect(() => {
    // to stop this code from running during initial mount
    if (currSq) {
      const i = currSq[0];
      const j = currSq[1];
      if (ends[i][j]) {
        setnextColor(boardSqs[i][j]);
      }
      else if (boardSqs[i][j] !== 'white' &&
               boardSqs[i][j] === nextColor) {
        let squares = boardSqs.slice(0);
        squares[i][j] = 'white';
        setboardSqs(squares);
      }
      // if square is white or is different than nextColor, set to nextColor
      else {
        console.log(currSq);
        let squares = boardSqs.slice(0);
        squares[i][j] = nextColor;
        setboardSqs(squares);
      }
    }
  }, [currSq]);

  if (!loaded) {
    return(
      <div className="game-info">
        Loading...
      </div>
    )
  }

  return(
    <div>
      {boardDisplay}
    </div>
  )
}

function Board(props) {
  const [loaded, setLoaded] = useState(false);
  const [response, setResponse] = useState(null);
  const [boardSqs, setboardSqs] = useState([]);
  const [ends, setEnds] = useState([]);
  const [currSq, setCurrSq] = useState();
  let numNotEnds = 0;

  useEffect(() => {
    // document.addEventListener('keydown', handleKeyDown);
    fetch("http://127.0.0.1:5000/play")
      .then(res => res.json())
      .then(result => setResponse(result));
  }, [])

  // const handleKeyDown = (e) => {
  //   // enter key
  //   if (currSq !== []) {
  //     if (e.keyCode === 13) {
  //       console.log('enter');
  //       handleClick(currSq[0], currSq[1]);
  //     }
  //     // left arrow
  //     else if (e.keyCode === 37) {
  //       console.log('left');
  //       if (currSq[1] !== 0) {
  //         let temp = [currSq[0], currSq[1] - 1];
  //         setCurrSq(temp);
  //       }
  //     }
  //     // right arrow
  //     else if (e.keyCode === 39) {
  //
  //       if (currSq[1] !== boardSqs.length - 1) {
  //         let temp = [currSq[0], currSq[1] + 1];
  //         setCurrSq(temp);
  //       }
  //     }
  //     // up arrow
  //     else if (e.keyCode === 38) {
  //       if (currSq[0] !== 0) {
  //         let temp = [currSq[0] - 1, currSq[1]];
  //         setCurrSq(temp);
  //       }
  //     }
  //     // down arrow
  //     else if (e.keyCode === 40) {
  //       if (currSq[0] !== boardSqs.length - 1) {
  //         let temp = [currSq[0] + 1, currSq[1]];
  //         setCurrSq(temp);
  //       }
  //     }
  //   }
  // }

  if (!response) {
    return (
      <div className="game-info">
        Loading...
      </div>
    )
  }

  else if (response && !loaded) {
    return (
      <div>
        <div className="game-info">
          Loading...
        </div>
        <Game
          setLoaded={setLoaded}
          response={response}
          numNotEnds={numNotEnds}
          boardSqs={boardSqs}
          setboardSqs={setboardSqs}
          ends={ends}
          setEnds={setEnds}
          currSq={currSq}
          setCurrSq={setCurrSq}
          loaded={loaded}
        />
      </div>
    )
  }

  return (
    <div>
      <Game
        setLoaded={setLoaded}
        response={response}
        numNotEnds={numNotEnds}
        boardSqs={boardSqs}
        setboardSqs={setboardSqs}
        ends={ends}
        setEnds={setEnds}
        currSq={currSq}
        setCurrSq={setCurrSq}
        loaded={loaded}
      />
      <GameInfo
        numNotEnds={numNotEnds}
        board={boardSqs}
      />
    </div>
  );
}

function GameInfo(props) {
  const numNotEnds = props.numNotEnds;
  const board = props.board;

  let numEmptySqs = 0;

  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board.length; j++) {
      if (board[i][j] === 'white') numEmptySqs++;
    }
  }

  return (
    <div>
      {Math.floor((1 - numEmptySqs/numNotEnds) * 100) + '% Completed'}
    </div>
  )
}

ReactDOM.render(
  <Board />,
  document.getElementById('root')
)
