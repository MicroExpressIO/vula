
class PromptVul():
    def __init__(self, role, goal, vul):
        self.prompt = {
            "role": f"{role}",
            "goal": f"{goal}",
            "requirement": f"""For the security problem defined in triple backtiks below, focus on Debian 10 and Debian 12, finish the tasks below (numbered items), need to verify the reliability of the output-update when necessary:
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
                
                    security problem: ```{vul}```
                    """
        }
    def get_prompt(self, cat):
        if cat == "req":
            return self.prompt["requirement"]
        if cat == "role":
            return self.prompt["role"]
        if cat == "goal":
            return self.prompt["goal"]

        return f"sth wrong"

