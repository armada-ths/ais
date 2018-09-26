import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import SignupQuestion from './SignupQuestion';
import uniqueId from 'lodash/uniqueId';
import axios from 'axios';

class App extends Component {
  constructor(props) {
    super(props);

    let questions = [];

    window.reactProps.questions && window.reactProps.questions.map(question => {
      question.arrayId = uniqueId();
      questions.push(question);
    });

    this.state = {
      questions,
      status: ''
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.addQuestion = this.addQuestion.bind(this);
    this.removeQuestion = this.removeQuestion.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    const form = document.getElementById('event-form');

    if (form.reportValidity()) {
      this.setState({status: ''});

      const formData = new FormData(form);

      formData.append('questions', JSON.stringify(this.state.questions));

      const currentUrl = window.location.href;
      axios.post(currentUrl, formData)
          .then(response => {
            this.setState({status: 'OK'})
          })
          .catch(response => {
            this.setState({status: 'Error'})
          });
    }
  }

  addQuestion() {
    this.setState(prevState => {
      let questions = [...prevState.questions];
      questions.push({
        type: 'text_field',
        question: '',
        required: false,
        options: [],
        arrayId: uniqueId()
      });
      return {
        questions
      }
    })
  }

  removeQuestion(arrayId) {
    this.setState(prevState => {
      return {
        questions: prevState.questions.filter(question => question.arrayId !== arrayId)
      }
    })
  }

  handleChange(arrayId, key, value) {
    this.setState(prevState => ({
      questions: prevState.questions.map(q => (q.arrayId === arrayId ? Object.assign({}, q, {[key]: value}) : q))
    }))
  }

  render() {
    const {status, questions} = this.state;
    const {question_types} = window.reactProps;

    return (
        <Fragment>
          <div className="panel panel-default">
            <div className="panel-heading">
              <h3 className="panel-title">Questions</h3>
            </div>
            <div className="panel-body">
              {questions.map(question =>
                  <SignupQuestion
                      removeQuestion={this.removeQuestion}
                      handleChange={(key, value) => this.handleChange(question.arrayId, key, value)}
                      key={question.arrayId}
                      questionTypes={question_types}
                      {...question}
                  />
              )}
              <button onClick={this.addQuestion} className="btn btn-primary">New Question</button>
            </div>
          </div>
          <button onClick={this.handleSubmit} className="btn btn-primary">Save</button>
          <span className="label label-success">{status}</span>
        </Fragment>
    )
  }
}

ReactDOM.render(
    <App/>,
    document.getElementById('react')
);
