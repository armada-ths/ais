from django.forms import Form, ModelForm
from .models import (
    Question,
    Response,
    Answer,
    TextAns,
    ChoiceAns,
    IntegerAns,
    BooleanAns,
)
from django.forms import (
    TextInput,
    Select,
    RadioSelect,
    ModelForm,
    Form,
    BooleanField,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
    ValidationError,
    IntegerField,
    CharField,
    ChoiceField,
)
from django.utils.text import slugify
from django import forms
from polymorphic.models import PolymorphicModel


class ResponseForm(ModelForm):
    WIDGETS = {
        Question.TEXT: forms.TextInput,
        Question.SELECT: forms.Select,
        Question.BOOL: forms.CheckboxInput,
        Question.INT: forms.NumberInput,
    }

    class Meta:
        model = Response
        fields = ()

    def __init__(self, survey, exhibitor=None, *args, **kwargs):
        self.survey = survey
        self.exhibitor = exhibitor
        super(ResponseForm, self).__init__(*args, **kwargs)
        # add a field for each survey question, corresponding to the question
        # type as appropriate.
        data = kwargs.get("data")
        for question in self.survey.questions.all():
            self.add_question(question, data)

    def add_question(self, question, data):
        """Add a question to the form.
        :param Question question: The question to add.
        :param dict data: The pre-existing values from a post request."""
        kwargs = {
            "label": question.text,
            "required": question.required,
        }
        initial = self.get_question_initial(question, data)
        if not initial is None:
            kwargs["initial"] = initial
        choices = self.get_question_choices(question)
        if choices:
            kwargs["choices"] = choices
        widget = self.get_question_widget(question)
        if widget:
            kwargs["widget"] = widget
        field = self.get_question_field(question, **kwargs)
        self.fields["question_%d" % question.pk] = (
            field  ## VERY IMPORTANT TO KEEP question_%d here. Other code is dependant on it
        )

    def get_question_initial(self, question, data):
        """Get the initial value that we should use in the Form
        :param Question question: The question
        :param dict data: Value from a POST request.
        :rtype: String or None"""
        initial = None
        answer = self._get_preexisting_answer(question)
        if answer:
            # Initialize the field with values from the database if any
            if question.question_type == Question.SELECT_MULTIPLE:
                initial = []
                if answer.ans == "[]":
                    pass
                elif "[" in answer.ans and "]" in answer.ans:
                    initial = []
                    unformated_choices = answer.ans[1:-1].strip()
                    for unformated_choice in unformated_choices.split(","):
                        choice = unformated_choice.split("'")[1]
                        initial.append(slugify(choice))
                else:
                    # Only one element
                    initial.append(slugify(answer.ans))
            else:
                initial = answer.ans
        if data:
            # Initialize the field field from a POST request, if any.
            # Replace values from the database
            initial = data.get("question_%d" % question.pk)
        if question.question_type == Question.INT:
            initial = 0
        return initial

    def _get_preexisting_answer(self, question):
        """Recover a pre-existing answer in database.
        The user must be logged. A Response containing the Answer must exists.
        :param Question question: The question we want to recover in the
        response.
        :rtype: Answer or None"""
        response = self._get_preexisting_response()
        if response is None:
            return None
        try:
            answer = Answer.objects.get(
                question=question, response=response
            ).get_real_instance()
            return answer
        except Answer.DoesNotExist:
            return None

    def _get_preexisting_response(self):
        """Recover a pre-existing response in database.
        The user must be logged in on exhibitor account
        :rtype: Response or None"""
        if self.exhibitor is None:
            return None
        try:
            return Response.objects.get(exhibitor=self.exhibitor, survey=self.survey)
        except Response.DoesNotExist:
            return None

    def get_question_widget(self, question):
        """Return the widget we should use for a question.
        :param Question question: The question
        :rtype: django.forms.widget or None"""
        try:
            return self.WIDGETS[question.question_type]
        except KeyError:
            return None

    def get_question_choices(self, question):
        """Return the choices we should use for a question.
        :param Question question: The question
        :rtype: List of String or None"""
        qchoices = None
        if question.question_type not in [Question.TEXT, Question.INT]:
            qchoices = question.get_choices()
            # add an empty option at the top so that the user has to explicitly
            # select one of the options
            if question.question_type in [Question.SELECT, Question.SELECT_IMAGE]:
                qchoices = tuple([("", "-------------")]) + qchoices
        return qchoices

    def get_question_field(self, question, **kwargs):
        """Return the field we should use in our form.
        :param Question question: The question
        :param **kwargs: A dict of parameter properly initialized in
            add_question.
        :rtype: django.forms.fields"""
        if question.question_type == Question.SELECT:
            return forms.ChoiceField(**kwargs)
        if question.question_type == Question.SELECT_MULTIPLE:
            return forms.MultipleChoiceField(**kwargs)
        if question.question_type == Question.INT:
            return forms.CharField(help_text="Answer ONLY with a number", **kwargs)
        ## This would be text, integer or bool.All are charfields with
        ## different widget arguments
        return forms.CharField(**kwargs)

    def save(self, commit=True):
        """Save the response object"""
        # Recover an existing response from the database if any
        #  There is only one response by logged user.
        response = self._get_preexisting_response()
        if response is None:
            response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.exhibitor = self.exhibitor
        response.save()
        # create an answer object for each question and associate it with this
        # response.
        for field_name, field_value in self.cleaned_data.items():
            if field_name.startswith("question_"):
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in
                # the field name in the __init__ method of this form class.
                q_id = int(field_name.split("_")[1])
                question = Question.objects.get(pk=q_id)
                answer = self._get_preexisting_answer(question)
                if answer is None:
                    if question.question_type == Question.INT:
                        answer = IntegerAns(question=question)
                        answer.ans = int(field_value)
                    if question.question_type == Question.TEXT:
                        answer = TextAns(question=question)
                        answer.ans = field_value
                    if question.question_type == Question.BOOL:
                        answer = BooleanAns(question=question)
                        answer.ans = bool(field_value)
                    if question.question_type == Question.SELECT:
                        answer = ChoiceAns(question=question)
                        answer.ans = field_value
                answer.response = response
                answer.save()
        return response
