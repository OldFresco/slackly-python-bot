import slacklybot
from StringIO import StringIO

def test_log_event_returns_expected_text():
    expected_output = "-- NEW EVENT LOG -- \n\nUSER: U5ZC51482\nCHANNEL: None\nTYPE: presence_change\nTEXT: None"
    out = StringIO()
    event = {u'type': u'presence_change',
             u'user': u'U5ZC51482', u'presence': u'active'}
    
    slacklybot.log_event(event, out=out)
    actual_output = out.getvalue().strip()
    
    assert actual_output == expected_output

def test_is_greeting_accurately_recognises_greeting():
    assert slacklybot.is_a_greeting('hi okay soo this is good') == True
    assert slacklybot.is_a_greeting('okay soo this is good') == False
    assert slacklybot.is_a_greeting('okay soo HI this is good') == True
    assert slacklybot.is_a_greeting('okay soo hellothis is good') == False
    assert slacklybot.is_a_greeting('okay HEY is good') == True
    assert slacklybot.is_a_greeting('yoyo') == False
    assert slacklybot.is_a_greeting('yo') == True

def test_is_a_opening_hours_query_accurately_recognises_opening_hours_query():
    assert slacklybot.is_a_opening_hours_query('What are your opening hours?') == True
    assert slacklybot.is_a_opening_hours_query('okay soo this is good') == False
    assert slacklybot.is_a_opening_hours_query('okay soo hi this is good') == False
    assert slacklybot.is_a_opening_hours_query('When are you open?') == True
    assert slacklybot.is_a_opening_hours_query('okay soo hellothis is good') == False
    assert slacklybot.is_a_opening_hours_query('What time can I call until?') == True
    assert slacklybot.is_a_opening_hours_query('okay hey hey is good') == False
    assert slacklybot.is_a_opening_hours_query('yoyo') == False
    assert slacklybot.is_a_opening_hours_query('Opening times') == True