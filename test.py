import slacklybot
from StringIO import StringIO

def test_log_event_returns_text():
    out = StringIO()
    event = {u'type': u'presence_change',
             u'user': u'U5ZC51482', u'presence': u'active'}
    
    slacklybot.log_event(event, out=out)
    output = out.getvalue().strip()
    assert output == '-- NEW EVENT...e\nTEXT: None'