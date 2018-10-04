import React, {PureComponent} from 'react';

class SignupQuestionOption extends PureComponent {
  render() {
    const {value, index, handleRemove, handleChange} = this.props;

    return (
        <li className="list-group-item">
          <div className="input-group">
            <input onChange={(event) => handleChange(event.target.value, index)} className="form-control" value={value}/>
            <div className="input-group-btn">
              <button onClick={() => handleRemove(index)} type="button" className="btn btn-default">
                <span className="glyphicon glyphicon-remove"/>
              </button>
            </div>
          </div>
        </li>)
  }

}

export default SignupQuestionOption;