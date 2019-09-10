import React, { useState } from 'react';
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
      <button
        className="square"
        style={{background: "white"}}
        onClick={props.onClick}>
        <button
          className="circle"
          style={{background: props.color}}
          onClick={props.onClick}
        />
      </button>
    )
  }
}

function Board(props) {
  const ends = props.ends;
  const [boardSqs, setboardSqs] = useState(props.colors);
  const [nextColor, setnextColor] = useState('white');

  let board = [];

  for (let i = 0; i < boardSqs.length; i++) {
    let children = [];
    for (let j = 0; j < boardSqs.length; j++) {
      children.push(<Square
                      key={(i.toString() + j.toString())}
                      color={boardSqs[i][j]}
                      ifEnd={ends[i][j]}
                      onClick={() => handleClick(i, j, ends, boardSqs, setboardSqs, nextColor, setnextColor)}
                    />);
    }
    board.push(<div
                className="board-row"
                key={i.toString()}>
                {children}
               </div>)
  }

  return (
    <div>
      {board}
    </div>
  );
}


function handleClick(i, j, ends, boardSqs, setboardSqs, nextColor, setnextColor) {
  // select the end to choose the next color
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

class GameImport extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      colors: [],
      ends: []
    }
  }

  componentDidMount() {
    fetch("http://127.0.0.1:5000/play")
      .then(res => res.json())
      .then(result => this.getBoard(result))
  }

  getBoard(input) {
    let colors = this.state.colors;
    let ends = this.state.ends;
    for (let i = 0; i < input.board.length; i++) {
      let thisRow = input.board[i];
      // allows for boards of different shapes and sizes
      colors.push([]);
      ends.push([]);
      for (let j = 0; j < thisRow.length; j++) {
        if (thisRow[j].length > 1) {
          ends[i].push(true);
          switch (thisRow[j]) {
            case 'rr':
              colors[i].push('red');
              break;
            case 'oo':
              colors[i].push('orange');
              break;
            case 'gg':
              colors[i].push('green');
              break;
            case 'yy':
              colors[i].push('yellow');
              break;
            case 'bb':
              colors[i].push('blue');
              break;
            case 'cc':
              colors[i].push('cyan');
              break;
            case 'pp':
              colors[i].push('purple');
              break;
            case 'mm':
              colors[i].push('maroon');
              break;
            default:
            // should not do this, means there is an error
              colors[i].push('pink');
          }
        }
        else {
          colors[i].push('white');
          ends[i].push(false);
        }
      }
    };
    this.setState({
      isLoaded: true,
      colors: colors,
      ends: ends
    })
  }

  render() {
    if (!this.state.isLoaded) {
      return (
        <div className="game-info">"Loading"</div>
      )
    } else {
      return (
        <Board
          colors={this.state.colors}
          ends={this.state.ends}
        />
      )
    }
  }
}

ReactDOM.render(
  <GameImport />,
  document.getElementById('root')
)
