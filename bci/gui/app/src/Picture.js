import React, { Component } from 'react'
import Img from 'react-image'
import axios from 'axios';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import Datetime from './Datetime'

export default class Picture extends Component {
    constructor(props) {
        super (props);
        this.state ={
            user: props.user,
            snapshot: props.snapshot,
            result: props.result,
            x: null,
            y: null,
            back: false,
        }
        this.back = this.back.bind(this);
    }
    componentDidMount() {
        return axios
        .get('http://127.0.0.1:5000/users/'+this.state.user+'/snapshots/'+this.state.snapshot+'/'+this.state.result,{headers: {'Content-Type': 'multipart/form-data'}},)
          .then(res=> 
            {
                console.log(this.state.result)
            this.setState (
              {x: res.data.height, y: res.data.width}
            )
          });
      }
      back(){
        this.setState({back: true})
    }
    render() {
        const {snapshot, user} = this.state;
        if( this.state.back === true){
            return (<BrowserRouter><div>
                <Route exact path={'/users/'+user+'/snapshots/'+snapshot}>
                 <Datetime user={user} snapshot={snapshot}/> 
                </Route>
                <Redirect to={'/users/'+user+'/snapshots/'+snapshot}/>
              </div>
            </BrowserRouter>);
        }
        return (
            <div style={ {marginLeft: 550}}>
                <button style={{position: 'absolute' ,top: 10, right: 10}} onClick ={this.back}>Back</button>
                <h1 style={{textDecoration: 'underline'}}>{this.state.result}</h1>
                <Img style={ { width: 480, height:270 }} src={'http://127.0.0.1:5000/users/'+this.state.user+'/snapshots/'+this.state.snapshot+'/'+this.state.result+'/data'}/>
            </div>
        )
    }
}
