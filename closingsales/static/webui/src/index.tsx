import React, { Component } from "react";
import { render } from "react-dom";

class SampleReact extends Component {
  render() {
    return <div>Hello World</div>;
  }
}

render(<SampleReact />, document.getElementById("closingshop"));
