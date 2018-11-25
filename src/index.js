import React from 'react';
import ReactDOM from 'react-dom';
import './game_ex.txt';
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
          {'❤'}
      </button>
    )
  }
}

class Board extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      squares: [['red', 'white', 'green', 'white', 'yellow'],
                ['white', 'white', 'blue', 'white', 'orange'],
                ['white', 'white', 'white', 'white', 'white'],
                ['white', 'green', 'white', 'yellow', 'white'],
                ['white', 'red', 'blue', 'orange', 'white']],
      ends: [[true, false, true, false, true],
             [false, false, true, false, true],
             [false, false, false, false, false],
             [false, true, false, true, false],
             [false, true, true, true, false]],
      nextColor: 'white',
    }
  }

  renderSquare(i, j) {
    return (
      <Square
        color={this.state.squares[i][j]}
        ifEnd={this.state.ends[i][j]}
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
    if (this.state.ends[i][j]) {
      this.setState({
        nextColor: this.state.squares[i][j]
      })
    }
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

ReactDOM.render(
  <Board />,
  document.getElementById('root')
)
