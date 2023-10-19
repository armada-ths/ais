import React, { PureComponent, useCallback, useEffect, useState } from 'react';
import Cookie from 'js-cookie';

import Grid from "@material-ui/core/es/Grid/Grid";
import TextField from "@material-ui/core/es/TextField/TextField";
import FormGroup from "@material-ui/core/es/FormGroup/FormGroup";
import FormControlLabel from "@material-ui/core/es/FormControlLabel/FormControlLabel";
import Checkbox from "@material-ui/core/es/Checkbox/Checkbox";
import Radio from "@material-ui/core/es/Radio/Radio";
import RadioGroup from "@material-ui/core/es/RadioGroup/RadioGroup";
import FormControl from "@material-ui/core/es/FormControl/FormControl";
import FormLabel from "@material-ui/core/es/FormLabel/FormLabel";
import NativeSelect from "@material-ui/core/es/NativeSelect/NativeSelect";
import xor from 'lodash/xor';
import includes from 'lodash/includes';
import { CircularProgress } from '@material-ui/core/es';

const FileUpload = ({ error, required, question, onChange }) => {
  const { upload_url } = window.reactProps

  const [file, setFile] = useState();
  const [fileUploadError, setFileUploadError] = useState();
  const [loading, setLoading] = useState(false);

  const handleFile = useCallback((file) => {
    setFile(file)
    setLoading(true)

    const formData = new FormData();
    formData.append('file', file);

    fetch(upload_url, {
      method: 'POST',
      body: formData,
      headers: {
        "X-CSRFToken": Cookie.get('csrftoken')
      }
    })
      .then(response => response.json().then(json => [json, response.status]))
      .then(([json, status]) => {
        console.log({ status, json })

        if (status !== 201) {
          const { reason: { file } } = json
          const error = file.map(v => v.message).join(', ')

          console.log({ file })

          setFileUploadError(error)
          setLoading(false)
          return
        }

        const { file_pk } = json

        onChange(`${file_pk}`)
        setFileUploadError(undefined)
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error:', error);
        setLoading(false)
      })
  }, [setFile])

  const hasError = !!(fileUploadError || error)

  const label = <>
    {question}
    {loading && <CircularProgress style={{ marginLeft: "0.5rem", display: 'inline-block' }} size="10" />}
  </>

  return (
    <FormControl error={hasError} component="fieldset" required={required}>
      <FormLabel component="legend">{label}</FormLabel>
      {fileUploadError && <FormLabel error>{fileUploadError}</FormLabel>}
      <TextField
        fullWidth
        required={required}
        value={file?.filename}
        error={hasError}
        onChange={(e) => handleFile(e.target.files[0])}
        accept="image/*,application/pdf"
        type="file"
      />
    </FormControl>
  )
}


class Question extends PureComponent {
  constructor() {
    super();
    this.handleMultiChoiceChange = this.handleMultiChoiceChange.bind(this);
  }

  handleMultiChoiceChange(toggledOption) {
    const { id, value, handleChange } = this.props;
    const updatedValue = xor(value, [toggledOption]);

    handleChange(id, updatedValue);
  }

  render() {
    const {
      id,
      value,
      error,
      question,
      type,
      options,
      required,
      handleChange,
    } = this.props;

    let answerElement;
    const student_programs = window.reactProps.student_programs;

    switch (type) {
      case 'text_field':
        answerElement = <TextField
          fullWidth
          required={required}
          label={question}
          value={value}
          error={error}
          onChange={(e) => handleChange(id, e.target.value)}
        />;
        break;
      case 'text_area':
        answerElement = <TextField
          fullWidth
          required={required}
          label={question}
          value={value}
          error={error}
          onChange={(e) => handleChange(id, e.target.value)}
          multiline
          rows={4}
        />;
        break;
      case 'single_choice': {
        answerElement = (
          <FormControl error={error} component="fieldset" required={required}>
            <FormLabel component="legend">{question}</FormLabel>
            <RadioGroup
              row
              value={value}
              onChange={(e) => handleChange(id, e.target.value)}
            >
              {options.map(option => <FormControlLabel
                key={option}
                label={option}
                value={option}
                control={
                  <Radio color="primary" />
                }
              />)}
            </RadioGroup>
          </FormControl>
        );
        break;
      }
      case 'multiple_choice': {
        answerElement = (
          <FormControl error={error} required component="fieldset">
            <FormLabel component="legend">{question}</FormLabel>
            <FormGroup row>
              {options.map(option => <FormControlLabel
                key={option}
                label={option}
                control={
                  <Checkbox
                    checked={includes(value, option)}
                    onChange={() => this.handleMultiChoiceChange(option)}
                    color="primary"
                  />
                } />)}
            </FormGroup>
          </FormControl>
        );
        break;
      }
      case 'student_program': {
        answerElement = (
          <FormControl error={error} component="fieldset" required={required}>
            <FormLabel component="legend">Choose your student program</FormLabel>
            <NativeSelect
              value={value}
              onChange={(e) => handleChange(id, e.target.value)}
            >
              <option value="" disabled={required}>Choose a program</option>
              {student_programs.map(option => <option
                key={option}
                label={option}
              >{option}</option>)}
            </NativeSelect>
          </FormControl>
        );
        break;
      }
      case 'file_upload': {
        answerElement = (
          <FileUpload error={error} required={required} question={question} onChange={v => handleChange(id, v)} />
        );
        break;
      }
    }

    return (
      <Grid item xs={12}>
        {answerElement}
      </Grid>
    )
  }
}

export default Question;
