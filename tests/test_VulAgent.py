import unittest
from unittest.mock import patch, MagicMock
from agent.VulAgent import LlmAdapter

class TestLlmAdapterCallGptSolution(unittest.TestCase):
    @patch("agent.VulAgent.OpenAI")
    @patch("agent.VulAgent.config")
    def test_call_gpt_solution_success(self, mock_config, mock_openai):
        # Setup mock config
        mock_config.doubao_url = "https://fake-url"
        mock_config.gpt_key = "fake-key"
        mock_config.gpt_model = "fake-model"

        # Setup mock OpenAI client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Test solution"
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        adapter = LlmAdapter("gpt_model")
        result = adapter.call_gpt_solution("system prompt", "user prompt")
        self.assertEqual(result, "Test solution")
        mock_client.chat.completions.create.assert_called_once()

    @patch("agent.VulAgent.OpenAI")
    @patch("agent.VulAgent.config")
    def test_call_gpt_solution_exception(self, mock_config, mock_openai):
        mock_config.doubao_url = "https://fake-url"
        mock_config.gpt_key = "fake-key"
        mock_config.gpt_model = "fake-model"

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API error")
        mock_openai.return_value = mock_client

        adapter = LlmAdapter("gpt_model")
        result = adapter.call_gpt_solution("system prompt", "user prompt")
        self.assertTrue(result.startswith("[GPT Calling exeption]"))
        self.assertIn("API error", result)

    ### manual test cases
    def test_gpt1():
        try:
            client = OpenAI(
                base_url="https://ark-ap-southeast.byteintl.net/api/v3",
                api_key="7385c60a-2ba0-45c4-8bc6-06d655719ad3"
            )

            print("----- standard request -----")
            response = client.chat.completions.create(

                model = "ep-20250922125042-zhl8s",
                messages = [
                    {"role": "system", "content": "You are an AI assistant"},
                    {"role": "user", "content": "What are the common cruciferous plants?"},
                ],
                reasoning_effort="medium"
            )

            if hasattr(response.choices[0].message, 'reasoning_content'):
                logging.debug("### start of reasoning_content")
                print(response.choices[0].message.reasoning_content)
                logging.debug("### end of reasoning_content")
            print(response.choices[0].message.content)
        except Exception as e:
            logging.exception(f"exception: {str(e)}")
            return 
    def test_call_gpt_solution():
        llma = llmAdapter = LlmAdapter("gpt_model")
        role = """ You are a experienced cyber security expert. """
        pmpt = """For the security problem defined in triple backtiks below, focus on Debian 10 and Debian 12, finish the tasks below (numbered items), need to verify the reliability of the output-update when necessary:
                        1. analyze the impact;
                        2. describe solution and give security best practices or mitigation steps;
                        3. give the remedaition scripts that can be run on both OS;
                            3.1 the scripts should be version specfic for the target software, avoid using 'the latest version' or 'the latest patch';
                            3.2 including depednecy check and verifciation for security vulnerability
                        4. list out the software version that fix the security problem if possible
                        5. add Triage section to analyze if the fix solution/script will impact running business, including below:
                            5.1. impact to any potential services / software that may depend on the current software
                            5.2 will it cause current service's running
                            5.3 will the solution case any network broken
                            5.4 any potential data lose
                            5.5 clearly suggestions if an online patching can be executed
                        6. for Debian 10, please consider research in 3rd party solution (Freexian is the paid 3rd party) if can not find the solution in public resources
                    
                        security problem: ```CVE-2024-53197```
                        """
        #ret = llma.call_gpt_solution("you are an AI assistant", "What are the common cruciferous plants?")
        ret = llma.call_gpt_solution(role, pmpt)
        print(f"ret: {ret}")

if __name__ == "__main__":
    unittest.main()