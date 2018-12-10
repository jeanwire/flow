import React from 'react';
import ReactDOM from 'react-dom';
import 'json-loader';
import gameBoard from './game_ex.json';
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
        style={{background: props.color}}
        onClick={props.onClick}>
          {'☼'}
      </button>
    )
  }
}

class Board extends React.Component {
  constructor(props) {
    super(props);
    // ends and colors initialized in GameImport
    this.ends = props.ends;
    this.state = {
      squares: props.colors,
      nextColor: 'white',
    }
  }

  renderSquare(i, j) {
    return (
      <Square
        color={this.state.squares[i][j]}
        ifEnd={this.ends[i][j]}
        onClick={() => this.handleClick(i, j)}
      />
    );
  }

  buildBoard = () => {
    let board = [];

    for (let i = 0; i < 5; i++) {
      let children = [];
      for (let j = 0; j < 5; j++) {
        children.push(this.renderSquare(i, j));
      }
      board.push(<div className="board-row">
                  {children}
                 </div>)
    }
    return board;
  };

  handleClick(i, j) {
    // select the end to choose the next color
    if (this.ends[i][j]) {
      this.setState({
        nextColor: this.state.squares[i][j]
      })
    }
    else if (this.state.squares[i][j] !== 'white' &&
             this.state.squares[i][j] === this.state.nextColor) {
      let squares = this.state.squares.slice(0);
      squares[i][j] = 'white';
      this.setState({
        squares: squares
      })
    }
    // if square is white or is different than nextColor, set to nextColor
    else {
      let squares = this.state.squares.slice(0);
      squares[i][j] = this.state.nextColor;
      this.setState({
        squares: squares
      })
    }
  }

  render() {
    return (
      <div>
        {this.buildBoard()}
      </div>
    );
  }
}

class GameImport extends React.Component {

  getBoard(input) {
    let colors = [];
    let ends = [];

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
    }
    return ({
      colors: colors,
      ends: ends
    })
  }

  render() {
    return (
      <Board
        colors={this.getBoard(gameBoard).colors}
        ends={this.getBoard(gameBoard).ends}
      />
    )
  }

}

ReactDOM.render(
  <GameImport />,
  document.getElementById('root')
)
