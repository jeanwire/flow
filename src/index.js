import React, { useState, useEffect } from 'react';
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

function Board(props) {
  const [loaded, setLoaded] = useState(false);
  const [ends, setEnds] = useState([]);
  const [boardSqs, setboardSqs] = useState([]);
  const [nextColor, setnextColor] = useState('white');
  const [currSq, setCurrSq] = useState([]);
  let numNotEnds = 0;

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    fetch("http://127.0.0.1:5000/play")
      .then(res => res.json())
      .then(result => getBoard(result));
  }, [])

  const getBoard = (input) => {
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
    setLoaded(true);
  }

  const buildBoard = () => {
    let board = [];

    for (let i = 0; i < boardSqs.length; i++) {
      let children = [];
      for (let j = 0; j < boardSqs.length; j++) {
        children.push(<Square
                        key={(i.toString() + j.toString())}
                        color={boardSqs[i][j]}
                        ifEnd={ends[i][j]}
                        onClick={() => handleClick(i, j)}
                      />);
        if (!ends[i][j]) numNotEnds++;
      }
      board.push(<div
                  className="board-row"
                  key={i.toString()}>
                  {children}
                 </div>)
    }
    return board;
  }

  const handleKeyDown = (e) => {
    // enter key
    if (currSq !== []) {
      if (e.keyCode === 13) {
        console.log('enter');
        handleClick(currSq[0], currSq[1]);
      }
      // left arrow
      else if (e.keyCode === 37) {
        console.log('left');
        if (currSq[1] !== 0) {
          let temp = [currSq[0], currSq[1] - 1];
          setCurrSq(temp);
        }
      }
      // right arrow
      else if (e.keyCode === 39) {

        if (currSq[1] !== boardSqs.length - 1) {
          let temp = [currSq[0], currSq[1] + 1];
          setCurrSq(temp);
        }
      }
      // up arrow
      else if (e.keyCode === 38) {
        if (currSq[0] !== 0) {
          let temp = [currSq[0] - 1, currSq[1]];
          setCurrSq(temp);
        }
      }
      // down arrow
      else if (e.keyCode === 40) {
        if (currSq[0] !== boardSqs.length - 1) {
          let temp = [currSq[0] + 1, currSq[1]];
          setCurrSq(temp);
        }
      }
    }
  }

  const handleClick = (i, j) => {
    // select the end to choose the next color
    const temp = [i, j];
    setCurrSq(temp);
    console.log('curr sq: ', currSq);
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
      let squares = boardSqs.slice(0);
      squares[i][j] = nextColor;
      setboardSqs(squares);
    }
  }

  if (!loaded) {
    return (
      <div className="game-info">
        Loading...
      </div>
    )
  }

  return (
    <div>
      {buildBoard()}
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
