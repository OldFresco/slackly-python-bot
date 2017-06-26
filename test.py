import slacklybot

def test_log_event_returns_the_right_text():
    assert slacklybot.logEvent() == '-- NEW EVENT LOG --'