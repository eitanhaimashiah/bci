import React, { Component } from 'react'
import axios from 'axios';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import Datetime from './Datetime';
import Inf from './Inf'

export default class Snapshots extends Component {
    constructor(props) {
        super(props);
        this.state = {
          snapshots: [],
          user: props.user,
          datetime: null,
          snapshot: null,
          back: false,
        };
        this.pass=this.pass.bind(this);
        this.back = this.back.bind(this);
      }
    
      componentDidMount() {
        return axios
        .get(sessionStorage.getItem('url')+'/users/'+this.state.user+'/snapshots',{headers: {'Content-Type': 'multipart/form-data'}},)
          .then(res=> {
            this.setState (
                { snapshots: res.data.snapshots }
                )
          });
      }
    
      pass(data){
        this.setState ({
        snapshot: data.snapshot_id,
        datetime: data.datetime
        })
      }
    
      back(){
        this.setState({back: true})
    }

      render() {
        const {snapshots, snapshot, user} = this.state;
        if( this.state.back === true){
            return (<BrowserRouter><div>
                <Route exact path={'/users/'+this.state.user}>
                 <Inf user={sessionStorage.getItem('user')}/> 
                </Route>
                <Redirect to={'/users/'+this.state.user}/>
              </div>
            </BrowserRouter>);
        }
        if(snapshot !== null){
          return (<BrowserRouter><div>
                     <Route exact path={'/users/'+user+'/snapshots/'+snapshot}>
                      <Datetime user={user} snapshot={snapshot} datetime={this.state.datetime}/>
                     </Route>
                     <Redirect to={'/users/'+user+'/snapshots/'+snapshot}/>
                   </div>
                 </BrowserRouter>);
        }
        
          return (<div style={ {marginLeft: 550}}>
              <button style={{position: 'absolute' ,top: 10, right: 10}} onClick ={this.back}>Back</button>
            <h1 style={{textDecoration: 'underline'}}>{'Snapshots'}</h1>
            <ul>
              {snapshots.map(snapshot => (
                <li style={{color: 'blue', textDecoration: 'underline'}} key={snapshot} onClick={()=>{this.pass(snapshot)}}>
                  Snapshot {snapshot.snapshot_id}: {snapshot.datetime}
                </li>
              ))}
            </ul>
            </div>
          );
      }
}
