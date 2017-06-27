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