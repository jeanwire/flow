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
  const [ends, setEnds] = useState([]);
  const [colors, setColors] = useState([]);
  const [lines, setLines] = useState([
    [[], [], [], [], []],
    [[], [], [], [], []],
    [[], [], [], [], []],
    [[], [], [], [], []],
    [[], [], [], [], []]
  ]);

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
    boardImport(boards[Number(gameNum) - 1]);
    // fetchBoard();
  }, []);

  // need to reconfigure flask app
  // const fetchBoard = async () => {
  //   let url = "10.0.13.200:5000/game/" + gameNum;
  //   try {
  //     let res = await fetch(url);
  //     let resJSON = await res.json();
  //     boardImport(resJSON);
  //   }
  //   catch (error) {
  //     console.error(error);
  //   }
  // }

  const boardImport = (board) => {
    let boardEnds = [];
    let boardColors = [];

    board.forEach(function(row) {
      let rowEnds = [];
      let rowColors = [];
      row.forEach(function(sq) {
        if (sq.length > 1) {
          rowEnds.push(true);
          switch(sq) {
            case 'rr':
              rowColors.push('red');
              break;
            case 'oo':
              rowColors.push('orange');
              break;
            case 'gg':
              rowColors.push('green');
              break;
            case 'yy':
              rowColors.push('yellow');
              break;
            case 'bb':
              rowColors.push('blue');
              break;
            case 'cc':
              rowColors.push('cyan');
              break;
            case 'pp':
              rowColors.push('purple');
              break;
            case 'mm':
              rowColors.push('maroon');
              break;
            default:
            // should not do this, means there is an error
              rowColors.push('pink');
          }
        }
        else {
          rowEnds.push(false);
          rowColors.push('white');
        };
      })
      boardEnds.push(rowEnds);
      boardColors.push(rowColors);
    });
    setEnds(boardEnds);
    setColors(boardColors);
    setLoaded(true);
  }

  const renderSquare = (i, j) => {
    if (ends[i][j]) {
      return (
        <View
          key={i.toString() + j.toString()}
          style={{...styles.square}}>
          <View
            style={{
              backgroundColor: colors[i][j],
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

    if (lines[i][j].length != 0) {
      let sqLines = lines[i][j];
      // will always have center circle
      centerOpacity = 1;
      if (sqLines.includes('u')) upOpacity = 1;
      if (sqLines.includes('l')) leftOpacity = 1;
      if (sqLines.includes('r')) rightOpacity = 1;
      if (sqLines.includes('d')) downOpacity = 1;
    }

    return (
      <View
        key={(i.toString() + j.toString())}
        style={{...styles.square}}>
          <View
            style={{
              ...styles.up,
              opacity: upOpacity,
              backgroundColor: colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.left,
              opacity: leftOpacity,
              backgroundColor: colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.center,
              opacity: centerOpacity,
              backgroundColor: colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.right,
              opacity: rightOpacity,
              backgroundColor: colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.down,
              opacity: downOpacity,
              backgroundColor: colors[i][j]
            }}
          />
      </View>
    )
  };

  const handleFingerDown = (evt, gs) => {
    const { pageX, pageY } = evt.nativeEvent;
    const row = Math.floor((pageY - 2 * styles.board.margin) / styles.square.height);
    const col = Math.floor((pageX - 2 * styles.board.margin) / styles.square.width);
    if (row >=0 && row < ends.length && col >= 0 && col < ends.length) {
      let currentLine = [[row, col]];
      let currDrawnLines = drawnLines;
      currDrawnLines.push(currentLine);

      if (ends[row][col]) {
        setNextColor(colors[row][col]);
        setPrevSq([row, col]);
        setdrawnLines(currDrawnLines);
      }
      else if (colors[row][col] != 'white') {
        // TODO: how to roll back lines?
        let currColors = colors.slice(0);
        currColors[row][col] = 'white';
        setdrawnLines(currDrawnLines);
        setColors(currColors);
      }
    }
  }

  const handleFingerDrag = (evt, gs) => {
    const { pageX, pageY } = evt.nativeEvent;
    const row = Math.floor((pageY - 2 * styles.board.margin) / styles.square.height);
    const col = Math.floor((pageX - 2 * styles.board.margin) / styles.square.width);
    if (row >=0 && row < ends.length && col >= 0 && col < ends.length) {
      let currColors = colors.slice(0);
      let currLines = lines.slice(0);
      if (!ends[row][col] && colors[row][col] != nextColor) {
        currColors[row][col] = nextColor;
        setColors(currColors);
      }
      if (row != prevSq[0] || col != prevSq[1]) {
        // for each new square added to the line, will be drawing either a horizontal or vertical line
        if (currLines[prevSq[0]][prevSq[1]].length === 2) {
          currLines[prevSq[0]][prevSq[1]].shift();
        }
        if (currLines[row][col].length === 2) {
          currLines[row][col].shift();
        }
        // line moving left
        if (col < prevSq[1]) {
          currLines[prevSq[0]][prevSq[1]].push('l');
          currLines[row][col].push('r');
        }
        // line moving right
        else if (col > prevSq[1]) {
          currLines[prevSq[0]][prevSq[1]].push('r');
          currLines[row][col].push('l');
        }
        // line moving up
        else if (row < prevSq[0]) {
          currLines[prevSq[0]][prevSq[1]].push('u');
          currLines[row][col].push('d');
        }
        // line moving down
        else if (row > prevSq[0]) {
          currLines[prevSq[0]][prevSq[1]].push('d');
          currLines[row][col].push('u');
        }
        setPrevSq([row, col]);
        setLines(currLines);
      }
    }
  };

  const buildBoard = () => {
    let board = [];
    for (let i = 0; i < ends.length; i++) {
      let children = [];
      for (let j = 0; j < ends.length; j++) {
        children.push(renderSquare(i, j));
      };

      board.push(<View
                    key={i.toString()}
                    style={{
                      flexDirection: 'row',
                    }}
                  >
                    {children}
                  </View>)
    }
    return board;
  };

  if (loaded) {
    return (
      <View
        style={{...styles.board}}
      >
        <View
          style={{...styles.board}}
          {...pr.panHandlers}
        >
          {buildBoard()}
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
    // TODO: make the placement of these squares nicer
    flex: 1,
    margin: 30,
    justifyContent: 'flex-start'
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
