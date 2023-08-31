import React, {Component} from 'react';
import map from 'lodash/map';
import classNames from 'classnames';
import SignupQuestionOption from "./SignupQuestionOption";

class SignupQuestion extends Component {
  constructor(props) {
    super(props);

    this.handleAddOption = this.handleAddOption.bind(this);
    this.handleChangeOption = this.handleChangeOption.bind(this);
    this.handleRemoveOption = this.handleRemoveOption.bind(this);
  }

  handleAddOption() {
    const {options, handleChange} = this.props;

    handleChange('options', [...options, '']);
  }

  handleChangeOption(value, index) {
    const {options, handleChange} = this.props;

    options[index] = value;

    handleChange('options', options);
  }

  handleRemoveOption(index) {
    const {options, handleChange} = this.props;
    options.splice(index, 1);
    handleChange('options', options);
  }

  render() {
    const {questionTypes, handleChange, removeQuestion, arrayId, required, question, type, options} = this.props;

    const typeOptions = map(questionTypes, (label, value) => <option key={value} value={value}>{label}</option>);

    const showQuestionOptions = (type === 'single_choice' || type === 'multiple_choice');

    return (
        <div className="row">
          <div className="form-group col-sm-2">
            <label htmlFor="type">Type</label>
            <select className="select form-control" name="type" value={type}
                    onChange={(e) => handleChange('type', e.target.value)}>
              {typeOptions}
            </select>
          </div>
          <div className={classNames("form-group", showQuestionOptions ? "col-sm-4" : "col-sm-8")}>
            <label htmlFor="question">Question</label>
            <input
                onChange={(e) => handleChange('question', e.target.value)}
                className="form-control" name="question" value={question}/>
          </div>
          {showQuestionOptions && (
              <div className="form-group col-sm-4">
                <label>Options</label>
                <div className="list-group">
                  {map(options, (value, index) => (
                          <SignupQuestionOption
                              key={index}
                              value={value}
                              index={index}
                              handleChange={this.handleChangeOption}
                              handleRemove={() => this.handleRemoveOption(index)}
                          />
                      )
                  )}
                  <button
                      type="button"
                      onClick={this.handleAddOption}
                      className="list-group-item"
                  >
                    Add
                  </button>
                </div>
              </div>
          )}

          <div className="form-group  col-sm-1">
            <label htmlFor="required">Required</label>
            <input
                name="required"
                type="checkbox"
                checked={required}
                onChange={(e) => handleChange('required', e.target.checked)}
            />
          </div>
          <div className="col-sm-1">
            <button
                type="button"
                style={{marginTop: '25px'}}
                className="btn btn-default"
                onClick={() => removeQuestion(arrayId)}>
              <span className="glyphicon glyphicon-remove"/>
            </button>
          </div>
        </div>
    )
  }
}

export default SignupQuestion;
