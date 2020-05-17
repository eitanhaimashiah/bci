import React, { Component } from 'react'
import axios from 'axios';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import Table from './Table'
import Picture from './Picture'
import Snapshots from './Snapshots';

export default class Datetime extends Component {
    constructor(props) {
        super(props);
        this.state = {
          results: [],
          user: props.user,
          snapshot: props.snapshot,
          result: null,
          back: false,
        };
        this.pass=this.pass.bind(this);
        this.back = this.back.bind(this);
      }
    
      componentDidMount() {
        return axios
        .get('http://127.0.0.1:5000/users/'+this.state.user+'/snapshots/'+this.state.snapshot,{headers: {'Content-Type': 'multipart/form-data'}},)
          .then(res=> {
            this.setState (
                { results: res.data.results }
                )
          });
      }
    
      pass(data){
        this.setState (
          { result: data }
        )
      }
      back(){
          this.setState({back: true})
      }
    
      render() {
        const {results, result, user,snapshot} = this.state;
        const date = new Date(snapshot*1)
        if( this.state.back === true){
            return (<BrowserRouter><div>
                <Route exact path={'/users/'+this.state.user+'/snapshots'}>
                 <Snapshots user={sessionStorage.getItem('user')}/> 
                </Route>
                <Redirect to={'/users/'+this.state.user+'/snapshots'}/>
              </div>
            </BrowserRouter>);
        }
        if(result !== null){
          if ((result === 'feelings') || (result === 'pose')){
                 return (<BrowserRouter><div>
                     <Route exact path={'/users/'+user+'/snapshots/'+snapshot+'/'+result}>
                      <Table user={user} snapshot={snapshot} result={result}/> 
                     </Route>
                     <Redirect to={'/users/'+user+'/snapshots/'+snapshot+'/'+result}/>
                   </div>
                 </BrowserRouter>);
                 }
            else {
                return (<BrowserRouter><div>
                    <Route exact path={'/users/'+user+'/snapshots/'+snapshot+'/'+result}>
                     <Picture user={user} snapshot={snapshot} result={result}/> 
                    </Route>
                    <Redirect to={'/users/'+user+'/snapshots/'+snapshot+'/'+result}/>
                  </div>
                </BrowserRouter>);
            }
        }
        
          return (<div style={ {marginLeft: 550}}>
              <button style={{position: 'absolute' ,top: 10, right: 10}} onClick ={this.back}>Back</button>
            <h1 style={{textDecoration: 'underline'}}>{date.toLocaleString()}</h1>
            <ul>
              {results.map(result => (
                <li style={{color: 'blue', textDecoration: 'underline'}} key={result} onClick={()=>{this.pass(result)}}>
                  {result}
                </li>
              ))}
            </ul>
            </div>
          );
      }
}
