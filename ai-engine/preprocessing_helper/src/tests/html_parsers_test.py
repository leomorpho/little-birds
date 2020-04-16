import config
import logging
import pytest
from ..parser import html_ingester

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class InputOutputTestCase():
    """Default input output test case"""
    def __init__(self, name, input, expected_output):
        self.name = name
        self.input = input
        self.expected_output = expected_output
        
class TestHtmlCleaner():
    html_to_clean = [
        InputOutputTestCase(
            name="",
            input="""<span class="pl-s1"><span class="pl-token" data-hydro-click="{&quot;event_type&quot;:&quot;code_navigation.click_on_symbol&quot;,&quot;payload&quot;:{&quot;action&quot;:&quot;click_on_symbol&quot;,&quot;repository_id&quot;:33884891,&quot;ref&quot;:&quot;master&quot;,&quot;language&quot;:&quot;Python&quot;,&quot;originating_url&quot;:&quot;https://github.com/apache/airflow/blob/master/airflow/models/dag.py&quot;,&quot;user_id&quot;:7016204}}" data-hydro-click-hmac="d5c0b5483771c151c381f07f0e385304d303f484a37a662a1883cabe23062ac9">conf</span></span>""",
            expected_output="""<span class="pl-s1"><span class="pl-token">conf</span></span>"""
        ),
        InputOutputTestCase(
            name="",
            input="""<div class="css-1k2abhj eqaamsw7"><h2 class="eqaamsw2 css-sy9xyy e1bu9qyp1"><div class="css-70qvj9 eqaamsw8"><div class="css-dxg4i7 eqaamsw6"><svg width="20px" height="20px" viewBox="0 0 24 24"><path d="M6.545 4.727a1.09 1.09 0 1 1 0-2.182H22.91a1.09 1.09 0 1 1 0 2.182H6.545zM1.636 2a1.636 1.636 0 1 1 0 3.273 1.636 1.636 0 0 1 0-3.273zm0 8.727a1.636 1.636 0 1 1 0 3.273 1.636 1.636 0 0 1 0-3.273zm0 8.728a1.636 1.636 0 1 1 0 3.272 1.636 1.636 0 0 1 0-3.272zm21.273-8.182a1.09 1.09 0 1 1 0 2.182H6.545a1.09 1.09 0 1 1 0-2.182H22.91zm0 8.727a1.09 1.09 0 1 1 0 2.182H6.545a1.09 1.09 0 1 1 0-2.182H22.91z"></path></svg></div>Description</div><span class="css-h5nqbc eqaamsw3"><svg width="16" height="16" viewBox="0 0 16 16" class="css-1vc2zc4 eqaamsw5"><path d="M10 7H.667C.298 7 0 7.448 0 8s.298 1 .667 1h14.666c.369 0 .667-.448.667-1s-.298-1-.667-1"></path></svg></span></h2></div>""",
            expected_output="""<div class="css-1k2abhj eqaamsw7"><h2 class="eqaamsw2 css-sy9xyy e1bu9qyp1"><div class="css-70qvj9 eqaamsw8"><div class="css-dxg4i7 eqaamsw6"><svg width="20px" height="20px"></svg></div>Description</div><span class="css-h5nqbc eqaamsw3"><svg width="16" height="16" class="css-1vc2zc4 eqaamsw5"></svg></span></h2></div>"""
        )
    ]
    
    @pytest.mark.parametrize("case", html_to_clean)
    def test_html_meta_splitting_cases(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = html_ingester.bare_html(case.input)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)