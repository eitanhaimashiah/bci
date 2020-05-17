/* eslint-disable require-jsdoc */
import React from 'react';
import './App.css';
import axios from 'axios';
import Inf from './Inf'
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      users: [],
      user: null,
    };
    this.pass=this.pass.bind(this);
  }

  componentDidMount() {
    return axios
    .get('http://127.0.0.1:5000/users',{headers: {'Content-Type': 'multipart/form-data'}},)
      .then(res=> {
       this.setState (
          { isLoaded: true,users: res.data.users }
        )
      });
  }

  pass(data){
    this.setState (
      { user: data }
    )
  }

  render() {
    const { error, isLoaded, users } = this.state;
    if(this.state.user !== null){
      return (<BrowserRouter><div>
                 <Route exact path={'/users/'+this.state.user}>
                  <Inf user={sessionStorage.getItem('user')}/> 
                 </Route>
                 <Redirect to={'/users/'+this.state.user}/>
               </div>
             </BrowserRouter>);
    }
    
      return (<div style={ {marginLeft: 550}}>
        <h1 style={{textDecoration: 'underline'}}>{'   Users     '}</h1>
        <ul>
          {users.map(user => (
            <li style={{color: 'blue', textDecoration: 'underline'}} key={user} onClick={()=>{this.pass(user)}}>
              {user}
            </li>
          ))}
        </ul>
        </div>
      );
    
  }
}

export default App;
