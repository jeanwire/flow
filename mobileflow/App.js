import React from 'react';
import { useState, useEffect } from 'react';
// this import is due to a bug in hooks in the current release
import 'babel-polyfill';
import { StyleSheet, Text, View, PanResponder, Button, FlatList } from 'react-native';

// need to reconfigure flask app - currently just serving boards locally
boards = [];
import {board as board1} from './game1.json';
boards.push(board1);
import {board as board2} from './game2.json';
boards.push(board2);
import {board as board3} from './game3.json';
boards.push(board3);
import {board as board4} from './game4.json';
boards.push(board4);
import {board as board5} from './game5.json';
boards.push(board5);



export default function App() {
  const [page, setPage] = useState('landingPage');
  const [gameNum, setGameNum] = useState(0);

  if (page === 'landingPage') {
    return <LandingPage
              setPage={setPage}
            />
  }
  else if (page === 'gameList') {
    return <GameSelection
              setPage={setPage}
              setGameNum={setGameNum}
            />
  }
  return <Board
            gameNum={gameNum}
            setPage={setPage}
          />;
}

function LandingPage(props) {
  const setPage = props.setPage;
  return(
    <View
      style={{...styles.container}}>
      <Text
        style={{...styles.text}}
      >
      {"Let's do the thing!"}
      </Text>
      <Button
        title="Click me!"
        color='purple'
        onPress={() => setPage('gameList')}
      />
    </View>
  )
}

function GameSelection(props) {
  const setPage = props.setPage;
  const setGameNum = props.setGameNum;

  let data = [];
  for (let i = 1; i <= 5; i++) {
    let title = 'Game ' + i;
    data.push({id: i.toString(), title: title});
  }

  return (
    <FlatList
      data={data}
      ListHeaderComponent={
        <Text
          style={{
            ...styles.text,
            marginTop: 20
          }}
        >
        Pick a game!
        </Text>
      }
      renderItem={({ item }) =>
        <Item
          title={item.title}
          id={item.id}
          setGameNum={setGameNum}
          setPage={setPage}
        />}
      keyExtractor={item => item.id}
    />
  )
}

function Item(props) {
  const title = props.title;
  const id = props.id;
  const setGameNum = props.setGameNum;
  const setPage = props.setPage;

  return (
    <View
      style={{
        margin: 5
      }}
    >
      <Button
        title={title}
        color='purple'
        onPress={() => {
          setGameNum(id);
          setPage('game');
        }}
      />
    </View>
  )
}

function Board(props) {

  const gameNum = props.gameNum;
  const setPage = props.setPage;
  let temp = [];
  for (let i  = 0; i < 25; i++) {
    temp.push({end: false,
              color: 'white',
              lines: [],
              id: i
            })
  }
  const [squares, setSquares] = useState(temp);

  // drawnLines will be used to roll back lines
  const [drawnLines, setdrawnLines] = useState([]);
  const [nextColor, setNextColor] = useState('white');
  const [prevSq, setPrevSq] = useState(null);
  const [loaded, setLoaded] = useState(false);

  const pr = PanResponder.create({
    onStartShouldSetPanResponder: (evt, gs) => true,
    onStartShouldSetPanResponderCapture: (evt, gs) => true,
    onMoveShouldSetPanResponder: (evt, gs) => true,
    onMoveShouldSetPanResponderCapture: (evt, gs) => true,
    onPanResponderGrant: (evt, gs) => {handleFingerDown(evt, gs)},
    onPanResponderMove: (evt, gs) => {handleFingerDrag(evt, gs)},
    onPanResponderRelease: (evt, gs) => {
      setNextColor('white')
    },
    onPanResponderTerminationRequest: (evt, gs) => true,
  });

  // board import
  useEffect(() => {
    // boardImport(boards[Number(gameNum) - 1]);
    fetchBoard();
  }, []);

  // need to reconfigure flask app
  const fetchBoard = async () => {
    let url = "http:10.0.13.200:5000/game/" + gameNum;
    try {
      let res = await fetch(url);
      let resJSON = await res.json();
      boardImport(resJSON.board);
    }
    catch (error) {
      console.error(error);
    }
  }

  const boardImport = (board) => {
    for (let col = 0; col < 5; col++) {
      for (let row = 0; row < 5; row++ ) {
        if (board[row][col].length > 1) {
          temp[row * 5 + col].end = true;
          switch(board[row][col]) {
            case 'rr':
              temp[row * 5 + col].color = 'red';
              break;
            case 'oo':
              temp[row * 5 + col].color = 'orange';
              break;
            case 'gg':
              temp[row * 5 + col].color = 'green';
              break;
            case 'yy':
              temp[row * 5 + col].color = 'yellow';
              break;
            case 'bb':
              temp[row * 5 + col].color = 'blue';
              break;
            case 'cc':
              temp[row * 5 + col].color = 'cyan';
              break;
            case 'pp':
              temp[row * 5 + col].color = 'purple';
              break;
            case 'mm':
              temp[row * 5 + col].color = 'maroon';
              break;
            default:
            // should not do this, means there is an error
              temp[row * 5 + col].color = 'pink';
          }
        }
        else {
          temp[row * 5 + col].end = false;
          temp[row * 5 + col].color = 'white';
        };
      }
    };
    setSquares(temp);
    setLoaded(true);
  }

  const handleFingerDown = (evt, gs) => {
    const { pageX, pageY } = evt.nativeEvent;
    const row = Math.floor((pageY - 2 * styles.board.margin) / styles.square.height);
    const col = Math.floor((pageX - 2 * styles.board.margin) / styles.square.width);
    if (row >=0 && row < 5 && col >= 0 && col < 5) {
      let currentLine = [[row, col]];
      let currDrawnLines = drawnLines;
      currDrawnLines.push(currentLine);

      if (squares[row * 5 + col].end) {
        setNextColor(squares[row * 5 + col].color);
        setPrevSq([row, col]);
        setdrawnLines(currDrawnLines);
      }
      else if (squares[row * 5 + col].color != 'white') {
        // TODO: how to roll back lines?
        let currSqs = squares.slice(0);
        currSqs[row * 5 + col].color = 'white';
        setdrawnLines(currDrawnLines);
        setSqs(currSqs);
      }
    }
  }

  const handleFingerDrag = (evt, gs) => {
    const { pageX, pageY } = evt.nativeEvent;
    const row = Math.floor((pageY - 2 * styles.board.margin) / styles.square.height);
    const col = Math.floor((pageX - 2 * styles.board.margin) / styles.square.width);
    if (prevSq && row >=0 && row < 5 && col >= 0 && col < 5) {
      let currSqs = squares.slice(0);
      if (!squares[row * 5 + col].end && squares[row * 5 + col].color != nextColor) {
        currSqs[row * 5 + col].color = nextColor;
        setSquares(currSqs);
      }
      if (row != prevSq[0] || col != prevSq[1]) {
        // for each new square added to the line, will be drawing either a horizontal or vertical line
        if (squares[prevSq[0] * 5 + prevSq[1]].lines.length === 2) {
          currSqs[prevSq[0] * 5 + prevSq[1]].lines.shift();
        }
        if (squares[row * 5 + col].lines.length === 2) {
          currSqs[row * 5 + col].lines.shift();
        }
        // line moving left
        if (col < prevSq[1]) {
          currSqs[prevSq[0] * 5 + prevSq[1]].lines.push('l');
          currSqs[row * 5 + col].lines.push('r');
        }
        // line moving right
        else if (col > prevSq[1]) {
          currSqs[prevSq[0] * 5 + prevSq[1]].lines.push('r');
          currSqs[row * 5 + col].lines.push('l');
        }
        // line moving up
        else if (row < prevSq[0]) {
          currSqs[prevSq[0] * 5 + prevSq[1]].lines.push('u');
          currSqs[row * 5 + col].lines.push('d');
        }
        // line moving down
        else if (row > prevSq[0]) {
          currSqs[prevSq[0] * 5 + prevSq[1]].lines.push('d');
          currSqs[row * 5 + col].lines.push('u');
        }
        setPrevSq([row, col]);
        setSquares(currSqs);
      }
    }
  };

  // const buildBoard = () => {
  //   let board = [];
  //   for (let i = 0; i < ends.length; i++) {
  //     let children = [];
  //     for (let j = 0; j < ends.length; j++) {
  //       children.push(renderSquare(i, j));
  //     };
  //
  //     board.push(<View
  //                   key={i.toString()}
  //                   style={{
  //                     flexDirection: 'row',
  //                   }}
  //                 >
  //                   {children}
  //                 </View>)
  //   }
  //   return board;
  // };

  if (loaded) {
    return (
      <View
        style={{...styles.board}}
      >
        <View
          style={{...styles.board, flex: 0, height: 242}}
          {...pr.panHandlers}
        >
          <FlatList
            data={squares}
            numColumns={5}
            renderItem={({ item }) =>
              <Square
                end={item.end}
                lines={item.lines}
                color={item.color}
                id={item.id}
              />}
            keyExtractor={item => item.id}
          />
        </View>
        <View style={{margin: 50}}>
          <Button
            title="Select New Game"
            color='purple'
            onPress={() => {
              setPage('gameList')}}
          />
        </View>
      </View>
    )
  }

  return (
    <View
      style={{...styles.container}}
    >
      <Text
        style={{...styles.text}}
      >
        Loading...
      </Text>
    </View>
  )
}

function Square(props) {
  const end = props.end;
  const lines = props.lines;
  const color = props.color;
  const id = props.id;
  if (end) {
    return (
      <View
        key={id.toString()}
        style={{...styles.square}}>
        <View
          style={{
            backgroundColor: color,
            ...styles.end
          }}/>
      </View>
    )
  };

  // if a line should appear, it becomes opaque
  let upOpacity = 0;
  let leftOpacity = 0;
  let centerOpacity = 0;
  let rightOpacity = 0;
  let downOpacity = 0;

  if (lines.length != 0) {
    // will always have center circle
    centerOpacity = 1;
    if (lines.includes('u')) upOpacity = 1;
    if (lines.includes('l')) leftOpacity = 1;
    if (lines.includes('r')) rightOpacity = 1;
    if (lines.includes('d')) downOpacity = 1;
  }

  return (
    <View
      key={id.toString()}
      style={{...styles.square}}>
        <View
          style={{
            ...styles.up,
            opacity: upOpacity,
            backgroundColor: color
          }}
        />
        <View
          style={{
            ...styles.left,
            opacity: leftOpacity,
            backgroundColor: color
          }}
        />
        <View
          style={{
            ...styles.center,
            opacity: centerOpacity,
            backgroundColor: color
          }}
        />
        <View
          style={{
            ...styles.right,
            opacity: rightOpacity,
            backgroundColor: color
          }}
        />
        <View
          style={{
            ...styles.down,
            opacity: downOpacity,
            backgroundColor: color
          }}
        />
    </View>
  )
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center'
  },
  text: {
    fontSize: 30,
    fontWeight: 'bold'
  },
  board: {
    flex: 1,
    margin: 29,
    justifyContent: 'flex-start',
    borderWidth: 1,
    borderColor: 'black'
  },
  square: {
    height: 50,
    width: 50,
    borderWidth: 1,
    borderColor: 'black',
    backgroundColor: 'white',
    margin: -1,
    justifyContent: 'flex-start',
    alignItems: 'flex-start'
  },
  end: {
    height: 48,
    width: 48,
    borderRadius: 48/2,
    margin: -0.5
  },
  up: {
    height: 25,
    width: 10,
    marginLeft: 20
  },
  down: {
    height: 25,
    width: 10,
    marginLeft: 20,
    marginTop: -5
  },
  left: {
    height: 10,
    width: 25,
    marginTop: -5
  },
  right: {
    height: 10,
    width: 25,
    marginLeft: 25,
    marginTop: -10
  },
  center: {
    height: 10,
    width: 10,
    borderRadius: 5,
    marginLeft: 20,
    marginTop: -10
  }
});
