/* eslint-disable require-jsdoc */
/* eslint linebreak-style: ["error", "unix"]*/
import React, {Component} from 'react';
import {BrowserRouter, Route, Redirect, Switch} from 'react-router-dom';
import './App.css';
import App from './App';
export default class Start extends Component {
  render() {
    return (
      <BrowserRouter >
        <div >
          <Switch>
            <Route exact path="/users">
              <App />
            </Route>
          </Switch>
          <Redirect to="/users" />
        </div>
      </BrowserRouter>
    );
  }
}
