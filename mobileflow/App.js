import React, { Component } from 'react';
import { useState } from 'react';
// this import is due to a bug in hooks in the current release
import 'babel-polyfill';
import { StyleSheet, Text, View, PanResponder, Button } from 'react-native';


export default function App() {
  const [page, setPage] = useState('landingPage');

  if (page == 'landingPage') {
    return <LandingPage
              page={page}
              setPage={setPage}
            />
  }
  return <Board/>;
}

function LandingPage(props) {
  const page = props.page;
  const setPage = props.setPage;
  return(
    <View
      style={{flex: 1,
              alignItems: 'center',
              justifyContent: 'center'}}>
      <Text>
      {"Let's do the thing!"}
      </Text>
      <Button
        title="Click me!"
        onPress={() => setPage('game')}
      />
    </View>
  )
}

class Board extends Component {
  constructor(props) {
    super(props);
    this.ends = [
      [true, false, true, false, true],
      [false, false, true, false, true],
      [false, false, false, false, false],
      [false, true, false, true, false],
      [false, true, true, true, false]
    ];
    this.state = {
      colors: [
        ['red', 'white', 'green', 'white', 'yellow'],
        ['white', 'white', 'blue', 'white', 'orange'],
        ['white', 'white', 'white', 'white', 'white'],
        ['white', 'green', 'white', 'yellow', 'white'],
        ['white', 'red', 'blue', 'orange', 'white']
      ],
      lines: [
        [[], [], [], [], []],
        [[], [], [], [], []],
        [[], [], [], [], []],
        [[], [], [], [], []],
        [[], [], [], [], []]
      ],
      nextColor: 'white',
      prevSq: null
    };
    this.pr = PanResponder.create({
      onStartShouldSetPanResponder: (evt, gs) => true,
      onStartShouldSetPanResponderCapture: (evt, gs) => true,
      onMoveShouldSetPanResponder: (evt, gs) => true,
      onMoveShouldSetPanResponderCapture: (evt, gs) => true,
      onPanResponderGrant: (evt, gs) => {this.handleFingerDown(evt, gs)},
      onPanResponderMove: (evt, gs) => {this.handleFingerDrag(evt, gs)},
      onPanResponderRelease: (evt, gs) => {
        this.setState({
          nextColor: 'white'
        })
      },
      onPanResponderTerminationRequest: (evt, gs) => true,
    })
  }

  renderSquare(i, j) {
    if (this.ends[i][j]) {
      return (
        <View
          key={i.toString() + j.toString()}
          style={{...styles.square}}>
          <View
            style={{
              backgroundColor: this.state.colors[i][j],
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

    if (this.state.lines[i][j].length != 0) {
      let lines = this.state.lines[i][j];
      // will always have center circle
      centerOpacity = 1;
      if (lines.includes('u')) upOpacity = 1;
      if (lines.includes('l')) leftOpacity = 1;
      if (lines.includes('r')) rightOpacity = 1;
      if (lines.includes('d')) downOpacity = 1;

    }

    return (
      <View
        key={(i.toString() + j.toString())}
        style={{...styles.square}}>
          <View
            style={{
              ...styles.up,
              opacity: upOpacity,
              backgroundColor: this.state.colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.left,
              opacity: leftOpacity,
              backgroundColor: this.state.colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.center,
              opacity: centerOpacity,
              backgroundColor: this.state.colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.right,
              opacity: rightOpacity,
              backgroundColor: this.state.colors[i][j]
            }}
          />
          <View
            style={{
              ...styles.down,
              opacity: downOpacity,
              backgroundColor: this.state.colors[i][j]
            }}
          />
      </View>
    )
  }

  handleFingerDown(evt, gs) {

    const { pageX, pageY } = evt.nativeEvent;
    const row = Math.floor((pageY - styles.container.margin) / styles.square.height);
    const col = Math.floor((pageX - styles.container.margin) / styles.square.width);
    if (row >=0 && row < this.ends.length && col >= 0 && col < this.ends.length) {
      let colors = this.state.colors.slice(0);
      // TODO: need to be able to roll back line
      if (this.ends[row][col]) {
        this.setState({
          nextColor: this.state.colors[row][col],
          prevSq: [row, col]
        })
      }
      else if (this.state.colors[row][col] != 'white') {
        // TODO: how should this behavior look?
        colors[row][col] = 'white';
        this.setState({
          colors: colors,
          prevSq: (row, col)
        })
      }
    }
  }

  handleFingerDrag(evt, gs) {
    const { pageX, pageY } = evt.nativeEvent;
    const row = Math.floor((pageY - styles.container.margin) / styles.square.height);
    const col = Math.floor((pageX - styles.container.margin) / styles.square.width);
    if (row >=0 && row < this.ends.length && col >= 0 && col < this.ends.length) {
      let colors = this.state.colors.slice(0);
      let lines = this.state.lines.slice(0);
      if (!this.ends[row][col] && colors[row][col] != this.state.nextColor) {
        colors[row][col] = this.state.nextColor;
        this.setState({
          colors: colors
        })
      }
      if (row != this.state.prevSq[0] || col != this.state.prevSq[1]) {
        let prevSq = this.state.prevSq;
        // for each new square added to the line, will be drawing either a horizontal or vertical line
        // line moving left
        if (col < this.state.prevSq[1]) {
          lines[prevSq[0]][prevSq[1]].push('l');
          lines[row][col].push('r');
        }
        // line moving right
        else if (col > this.state.prevSq[1]) {
          lines[prevSq[0]][prevSq[1]].push('r');
          lines[row][col].push('l');
        }
        // line moving up
        else if (row < this.state.prevSq[0]) {
          lines[prevSq[0]][prevSq[1]].push('u');
          lines[row][col].push('d');
        }
        // line moving down
        else if (row > this.state.prevSq[0]) {
          lines[prevSq[0]][prevSq[1]].push('d');
          lines[row][col].push('u');
        }
        this.setState({
          prevSq: [row, col],
          lines: lines
        })
      }
    }
  }

  buildBoard() {
    let board = [];
    for (let i = 0; i < this.ends.length; i++) {
      let children = [];
      for (let j = 0; j < this.ends.length; j++) {
        children.push(this.renderSquare(i, j));
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
  }

  render() {
    return (
      <View
        style={{...styles.container}}
        {...this.pr.panHandlers}
      >
        {this.buildBoard()}
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
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
