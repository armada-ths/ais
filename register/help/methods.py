from django.utils import timezone
from django.utils.timezone import utc

from fair.models import Fair
from register.models import SignupLog
from orders.models import Order
from matching.models import Survey, Question, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns

import datetime

def get_time_flag(close_offset = 7, warning_offset = 7):
    # used to close cr, a warning text after deadline will pop up, however exhibitors will not be permitted to do any changes after the offset in days has passed
    currentFair = None
    try:
        currentFair = Fair.objects.get(current=True)
        if currentFair.complete_registration_close_date:
            end_time = currentFair.complete_registration_close_date.replace(tzinfo=utc)
            end_time_close = end_time + datetime.timedelta(days=close_offset)
            time = datetime.datetime.now().replace(tzinfo=utc)
            time = time.replace(microsecond=0)
            warning_time = end_time - datetime.timedelta(days=warning_offset)
            if time < end_time and time > warning_time:
                return('warning', [end_time, end_time - time])
            elif time > end_time and time < end_time_close:
                return('overdue', [end_time, time - end_time])
            elif time > end_time_close:
                return('closed', [end_time, time - end_time])
            else:
                return(None, [None, None])
        else:
            return(None, [None, None])
    except Fair.DoesNotExist:
        return(None, [None, None])


# Contract agreement
def create_signup(contact, contract):
    signup = None
    try:
        signup = SignupLog.objects.get(contact=contact, contract=contract, company = contact.belongs_to)
    except SignupLog.DoesNotExist:
        signup = SignupLog.objects.create(contact=contact, contract=contract, company = contact.belongs_to, type = 'complete')


# create or update orders to the current exhibitor from products
def create_or_update_order(product, amount, exhibitor):
    order = None
    try:
        order = Order.objects.get(product=product, exhibitor=exhibitor)
        order.amount = amount
        order.save()
    except Order.DoesNotExist:
        order = Order.objects.create(
            exhibitor=exhibitor,
            product=product,
            amount=amount,
        )


# delete an order via a product and the current exhibitor
def delete_order_if_exists(product, exhibitor):
    try:
        Order.objects.get(product=product, exhibitor=exhibitor).delete()
    except Order.DoesNotExist:
        return

def product_amount_string(product, amount):
    return product.name + " x " + str(amount) + "\n"


def create_or_update_answer(response, question, ans):
    answer = None
    if question.question_type == Question.TEXT:
        try:
            answer = TextAns.objects.get(question=question, response=response)
            answer.ans = ans
            answer.save()
        except TextAns.DoesNotExist:
            answer = TextAns.objects.create(question=question, response = response, ans=ans)
    elif question.question_type == Question.INT:
        try:
            answer = IntegerAns.objects.get(question=question, response=response)
            answer.ans = ans
            answer.save()
        except IntegerAns.DoesNotExist:
            answer = IntegerAns.objects.create(question=question, response = response, ans=ans)
    elif question.question_type == Question.SELECT:
        try:
            answer = ChoiceAns.objects.get(question=question, response=response)
            answer.ans = ans
            answer.save()
        except ChoiceAns.DoesNotExist:
            answer = ChoiceAns.objects.create(question=question, response = response, ans=ans)
    elif question.question_type == Question.BOOL:
        try:
            answer = BooleanAns.objects.get(question=question, response=response)
            answer.ans = ans
            answer.save()
        except BooleanAns.DoesNotExist:
            answer = BooleanAns.objects.create(question=question, response = response, ans=ans)


# create or update responses on matching questions
def create_or_update_response(question, ans, exhibitor):
    response = None
    try:
        response = Response.objects.get(exhibitor=exhibitor, question=question, survey=matching_survey)
        #response.save()
    except Response.DoesNotExist:
        response = Response.objects.create(exhibitor=exhibitor, survey=matching_survey, question=question)
    create_or_update_answer(response, question, ans)


#delete response via question and current exhibitor
def delete_response_if_exists(question, ans, exhibitor):
    try:
        Response.objects.get(exhibitor=exhibitor, survey=matching_survey, question=question).delete()
    except Response.DoesNotExist:
        return
