import React, { Component } from 'react'
import axios from 'axios';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import { Container, Grid, Header, List } from "semantic-ui-react";
import Snapshots from './Snapshots';
import App from './App';

export default class Inf extends Component {
    constructor(props) {
        super (props);
        this.state ={
            user: props.user,
            birthday: null,
            gender: null,
            user_id: null,
            username: null,
            snapshots: false,
            back: false,
        }
        this.pass=this.pass.bind(this);
        this.back = this.back.bind(this);
    }
    componentDidMount() {
        return axios
        .get('http://127.0.0.1:5000/users/'+this.state.user,{headers: {'Content-Type': 'multipart/form-data'}},)
          .then(res=> {
           this.setState (
              { birthday: res.data.birthday, gender: res.data.gender, user_id: res.data.user_id, username: res.data.username}
            )
          });
      }
    
      pass(){
        this.setState (
          { snapshots: true }
        )
      }
      back(){
        this.setState({back: true})
    }
    render() {
        const inf =['birthday','gender', 'user_id', 'username']
        if( this.state.back === true){
            return (
                <BrowserRouter >
                  <div >
                      <Route exact path="/users">
                        <App />
                      </Route>
                    <Redirect to="/users" />
                  </div>
                </BrowserRouter>)
        }
        if(this.state.snapshots === true){
            return (<BrowserRouter><div>
                <Route exact path={'/users/'+this.state.user+'/snapshots'}>
                 <Snapshots user={sessionStorage.getItem('user')}/> 
                </Route>
                <Redirect to={'/users/'+this.state.user+'/snapshots'}/>
              </div>
            </BrowserRouter>);
        }
        const date = new Date(this.state.birthday*1000)
        return (
            <div style={ {marginLeft: 550}}>
                <button style={{position: 'absolute' ,top: 10, right: 10}} onClick ={this.back}>Back</button>
                <h1 style={{textDecoration: 'underline'}}>User  {this.state.user}</h1>
                <table>
                    <tbody>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[0]}</td>
                            <td>{date.toLocaleDateString()}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[1]}</td>
                            <td>{this.state.gender}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[2]}</td>
                            <td>{this.state.user_id}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[3]}</td>
                            <td>{this.state.username}</td>
                        </tr>
                    </tbody>
                </table>
                <button onClick={this.pass}>snapshots</button>
            </div>
        )
    }
}
