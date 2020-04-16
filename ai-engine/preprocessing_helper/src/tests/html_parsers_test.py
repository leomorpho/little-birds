import config
import logging
import pytest
from lxml import etree
from ..parser import html_ingester

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class InputOutputTestCase():
    """Default input output test case"""
    def __init__(self, name, input, expected_output):
        self.name = name
        self.input = input
        self.expected_output = expected_output


class TestCustomHtmlTarget():
    class HtmlEtreeParsingTestCase():
        """Default input output test case"""
        def __init__(self, 
                    name, 
                    input, 
                    short_text, 
                    full_text, 
                    meta, 
                    meta_words_of_interest):
            self.name = name
            self.input = input
            self.short_text = short_text
            self.full_text = full_text
            self.meta = meta
            self.meta_words_of_interest = meta_words_of_interest
        
    @pytest.fixture
    def custom_html_target_parser(self):
        return etree.HTMLParser(
            target=html_ingester.CustomHtmlTarget(), 
            remove_blank_text=True,
            remove_comments=True,
            remove_pis=True)
    
    to_feed_to_parser = [
        HtmlEtreeParsingTestCase(
            name="",
            input="""<span class="pl-s1"><span class="pl-token" data-hydro-click="{&quot;event_type&quot;:&quot;code_navigation.click_on_symbol&quot;,&quot;payload&quot;:{&quot;action&quot;:&quot;click_on_symbol&quot;,&quot;repository_id&quot;:33884891,&quot;ref&quot;:&quot;master&quot;,&quot;language&quot;:&quot;Python&quot;,&quot;originating_url&quot;:&quot;https://github.com/apache/airflow/blob/master/airflow/models/dag.py&quot;,&quot;user_id&quot;:7016204}}" data-hydro-click-hmac="d5c0b5483771c151c381f07f0e385304d303f484a37a662a1883cabe23062ac9">conf</span></span>""",
            short_text=["conf"],
            full_text=["conf"],
            meta=[],
            meta_words_of_interest=[]
        )
    ]
    @pytest.mark.parametrize("case", to_feed_to_parser)
    def test_custom_html_target_parser(self, case, custom_html_target_parser):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = etree.HTML(case.input, custom_html_target_parser)
        log.debug("Result short_text " + str(result.short_text))
        log.debug("Result full_text " + str(result.full_text))
        log.debug("Result meta " + str(result.meta))
        log.debug("Result meta_words_of_interest " \
            + str(result.meta_words_of_interest))
        assert(result.short_text == case.short_text)
        assert(result.full_text == case.full_text)
        assert(result.meta == case.meta)
        assert(result.meta_words_of_interest == case.meta_words_of_interest)

  
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
    def test_html_bare_cleaner(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = html_ingester.bare_html(case.input)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)