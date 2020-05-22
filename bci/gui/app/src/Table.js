import React, { Component } from 'react'
import axios from 'axios';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import Datetime from './Datetime'

export default class Table extends Component {
    constructor(props) {
        super (props);
        this.state ={
            user: props.user,
            snapshot: props.snapshot,
            result: props.result,
            exhaustion: null,
            happiness: null,
            hunger: null,
            thirst: null,
            rw: null,
            rx: null,
            ry: null,
            rz: null,
            tx: null,
            ty: null,
            tz: null,
            back: false,
        }
        this.back = this.back.bind(this);
    }
    componentDidMount() {
        return axios
        .get('http://127.0.0.1:5000/users/'+this.state.user+'/snapshots/'+this.state.snapshot+'/'+this.state.result,{headers: {'Content-Type': 'multipart/form-data'}},)
          .then(res=> {
            if(this.state.result === 'pose')
            {
                console.log(res)
                this.setState (
               { rw: res.data.rotation.w, rx:res.data.rotation.x, ry: res.data.rotation.y, rz: res.data.rotation.z, tx: res.data.translation.x, ty: res.data.translation.y, tz: res.data.translation.z}
             )}

           else if(this.state.result === 'feelings')
           {this.setState (
              { exhaustion: res.data.exhaustion, happiness: res.data.happiness, hunger: res.data.hunger, thirst: res.data.thirst }
            )}
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
        if (this.state.result === 'feelings')
        {const inf =['exhaustion','happiness', 'hunger', 'thirst']
        return (
            <div style={ {marginLeft: 550}}>
                <button style={{position: 'absolute' ,top: 10, right: 10}} onClick ={this.back}>Back</button>
                <h1 style={{textDecoration: 'underline'}}>{this.state.result}</h1>
                <table>
                    <tbody>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[0]}</td>
                            <td>{this.state.exhaustion}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[1]}</td>
                            <td>{this.state.happiness}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[2]}</td>
                            <td>{this.state.hunger}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[3]}</td>
                            <td>{this.state.thirst}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )}
        const inf =['w','x', 'y', 'z']
        return (
            <div style={ {marginLeft: 550}}>
                <button style={{position: 'absolute' ,top: 10, right: 10}} onClick ={this.back}>Back</button>
                <h1 style={{textDecoration: 'underline'}}>{this.state.result}</h1>
                <h3 style={{textDecoration: 'underline'}}>rotation</h3>
                <table>
                    <tbody>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[0]}</td>
                            <td>{this.state.rw}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[1]}</td>
                            <td>{this.state.rx}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[2]}</td>
                            <td>{this.state.ry}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[3]}</td>
                            <td>{this.state.rz}</td>
                        </tr>
                    </tbody>
                </table>
                <h3 style={{textDecoration: 'underline'}}>translation</h3>
                <table>
                    <tbody>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[1]}</td>
                            <td>{this.state.tx}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[2]}</td>
                            <td>{this.state.ty}</td>
                        </tr>
                        <tr>
                            <td style={{fontWeight: 'bold'}}>{inf[3]}</td>
                            <td>{this.state.tz}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }
}
