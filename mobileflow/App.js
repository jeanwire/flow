import React, { Component } from 'react';
import { StyleSheet, Text, View, PanResponder } from 'react-native';

export default class Board extends Component {
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
      squares: [
        ['red', 'white', 'green', 'white', 'yellow'],
        ['white', 'white', 'blue', 'white', 'orange'],
        ['white', 'white', 'white', 'white', 'white'],
        ['white', 'green', 'white', 'yellow', 'white'],
        ['white', 'red', 'blue', 'orange', 'white']
      ],
      nextColor: 'white'
    };
    this.pr = PanResponder.create({
      onStartShouldSetPanResponder: (evt, gs) => true,
      onStartShouldSetPanResponderCapture: (evt, gs) => true,
      onMoveShouldSetPanResponder: (evt, gs) => true,
      onMoveShouldSetPanResponderCapture: (evt, gs) => true,
      onPanResponderGrant: (evt, gs) => this.handleFingerDown(evt, gs),
      onPanResponderMove: (evt, gs) => this.handleFingerDrag(evt, gs),
      // onPanResponderRelease -> yes, to change next color
      onPanResponderTerminationRequest: (evt, gs) => true,
      // onPanResponderTerminate -> yes, to change next color
    })
  }

  renderSquare(i, j) {
    if (this.ends[i][j]) {
      return (
        <View
        key={(i.toString() + j.toString())}
        style={{
          backgroundColor: this.state.squares[i][j],
          ...styles.end}}/>
      )
    };

    return (
      <View
      key={(i.toString() + j.toString())}
      style={{
        backgroundColor: this.state.squares[i][j],
        ...styles.square}}/>
    )
  }

  handleFingerDown(evt, gs) {
    const { pageX, pageY } = evt.nativeEvent;
    const row = Math.floor((pageY - styles.container.margin) / styles.square.height);
    const col = Math.floor((pageX - styles.container.margin) / styles.square.width);
    let squares = this.state.squares.slice(0);
    // TODO: need to be able to roll back line
    if (this.ends[row][col]) {
      this.setState({
        nextColor: this.state.squares[row][col]
      })
    }
    if (this.state.squares[row][col] == 'white') {
      // TODO: how should this behavior look?
      squares[row][col]
    }
  }

  handleFingerDrag(evt, gs) {

  }

  buildBoard() {
    let board = [];
    for (let i = 0; i < 5; i++) {
      let children = [];
      for (let j = 0; j < 5; j++) {
        children.push(this.renderSquare(i, j));
      };

      board.push(<View
                  style={{
                    flex: 1,
                    flexDirection: 'row',
                  }}>
                  {children}
                </View>)
    }
    return board;
  }

  render() {
    return (
      <View style={{...styles.container}}>
        {this.buildBoard()}
      </View>
    )
  }

}

const styles = StyleSheet.create({
  container: {
    height: 250,
    margin: 30,
    alignItems: 'center',
    justifyContent: 'center'
  },
  square: {
    height: 50,
    width: 50,
    borderWidth: 1,
    borderColor: 'black'
  },
  end: {
    height: 50,
    width: 50,
    borderRadius: 50/2
  }
});
