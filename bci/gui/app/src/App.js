/* eslint-disable require-jsdoc */
import React from 'react';
import './App.css';
import axios from 'axios';
import Inf from './Inf'
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import settings from './settings.json'
sessionStorage.setItem('url', 'http://'+settings['DEFAULT_API_SERVER_HOST']+':'+settings['DEFAULT_API_SERVER_PORT'])
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
    .get(sessionStorage.getItem('url')+'/users',{headers: {'Content-Type': 'multipart/form-data'}},)
      .then(res=> {
       this.setState (
          { isLoaded: true,users: res.data.users }
        )
      });
  }

  pass(data){
    sessionStorage.setItem('user', data)
    this.setState (
      { user: data }
    )
  }

  render() {
    const { error, isLoaded, users } = this.state;
    if(this.state.user !== null ){
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
